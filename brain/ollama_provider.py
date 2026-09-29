import ollama

from threading import Event

from brain.provider import ModelProvider


class OllamaProvider(ModelProvider):

    def __init__(
        self,
        host,
        model,
    ):

        self.host = host

        self.model = model

        self.client = ollama.Client(
            host=host
        )

        self.last_error = None

        # -----------------------------------------------------
        # Provider cancellation state
        # -----------------------------------------------------

        self._cancel_event = Event()

        self._active_stream = None

    # =========================================================
    # CANCELLATION
    # =========================================================

    def cancel(self):

        self._cancel_event.set()

        stream = self._active_stream

        if stream is not None:

            close = getattr(
                stream,
                "close",
                None,
            )

            if callable(close):

                try:
                    close()
                except Exception:
                    pass

        return True

    def reset_cancellation(self):

        self._cancel_event.clear()

    # =========================================================
    # GENERATE
    # =========================================================

    def generate(
        self,
        messages,
        **kwargs,
    ):

        try:

            self.reset_cancellation()

            options = {
                "keep_alive": "10m",
                **kwargs,
            }

            response = self.client.chat(
                model=self.model,
                messages=messages,
                **options,
            )

            if self._cancel_event.is_set():

                return ""

            self.last_error = None

            return response[
                "message"
            ][
                "content"
            ]

        except Exception as error:

            self.last_error = str(
                error
            )

            raise RuntimeError(
                f"Ollama generation failed: {error}"
            ) from error

    # =========================================================
    # STREAM
    # =========================================================

    def stream(
        self,
        messages,
        **kwargs,
    ):

        self.reset_cancellation()

        stream = None

        try:

            options = {
                "keep_alive": "10m",
                **kwargs,
            }

            stream = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                **options,
            )

            self._active_stream = stream

            for chunk in stream:

                # -------------------------------------------------
                # Cancellation is checked before processing every
                # chunk.
                # -------------------------------------------------

                if self._cancel_event.is_set():

                    break

                content = chunk.get(
                    "message",
                    {},
                ).get(
                    "content",
                    "",
                )

                if not content:

                    continue

                yield content

                # -------------------------------------------------
                # Check again immediately after emitting a chunk.
                # -------------------------------------------------

                if self._cancel_event.is_set():

                    break

            if self._cancel_event.is_set():

                return

            self.last_error = None

        except Exception as error:

            # -----------------------------------------------------
            # Cancellation is not treated as an application error.
            # -----------------------------------------------------

            if self._cancel_event.is_set():

                return

            self.last_error = str(
                error
            )

            raise RuntimeError(
                f"Ollama streaming failed: {error}"
            ) from error

        finally:

            self._active_stream = None

            close = getattr(
                stream,
                "close",
                None,
            )

            if callable(close):

                try:
                    close()
                except Exception:
                    pass

    # =========================================================
    # WARMUP
    # =========================================================

    def warmup(self):

        try:

            self.reset_cancellation()

            self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Reply with OK.",
                    }
                ],
                options={
                    "num_predict": 1,
                },
                keep_alive="10m",
            )

            self.last_error = None

            return True

        except Exception as error:

            self.last_error = str(
                error
            )

            return False

    # =========================================================
    # HEALTH
    # =========================================================

    def health(self):

        try:

            self.client.list()

            self.last_error = None

            return True

        except Exception as error:

            self.last_error = str(
                error
            )

            return False