from threading import Event

from PySide6.QtCore import (
    QObject,
    Signal,
    QThread,
)


class ChatWorker(QObject):

    chunk = Signal(str)

    finished = Signal()

    stopped = Signal()

    error = Signal(str)

    def __init__(
        self,
        krish,
        message,
    ):

        super().__init__()

        self.krish = krish

        self.message = message

        self._cancel_event = Event()

    # =========================================================
    # CANCEL
    # =========================================================

    def cancel(self):

        self._cancel_event.set()

        # -----------------------------------------------------
        # If the KRISH/provider layer exposes cancellation,
        # request it immediately.
        # -----------------------------------------------------

        try:

            provider = (
                self.krish.router.select()
            )

            cancel = getattr(
                provider,
                "cancel",
                None,
            )

            if callable(cancel):

                cancel()

        except Exception:

            pass

    # =========================================================
    # RUN
    # =========================================================

    def run(self):

        stopped = False

        try:

            stream_method = getattr(
                self.krish,
                "stream_chat_message",
                None,
            )

            if not callable(
                stream_method
            ):

                raise RuntimeError(
                    "KRISH streaming interface is unavailable."
                )

            # -------------------------------------------------
            # Pass cancellation into the KRISH stream when the
            # interface supports it.
            # -------------------------------------------------

            try:

                stream = stream_method(
                    self.message,
                    cancel_event=self._cancel_event,
                )

            except TypeError:

                # -------------------------------------------------
                # Backward compatibility with the existing KRISH
                # interface.
                # -------------------------------------------------

                stream = stream_method(
                    self.message
                )

            for piece in stream:

                if self._cancel_event.is_set():

                    stopped = True

                    break

                self.chunk.emit(
                    str(piece)
                )

            if self._cancel_event.is_set():

                stopped = True

            if stopped:

                self.stopped.emit()

            else:

                self.finished.emit()

        except Exception as error:

            if self._cancel_event.is_set():

                self.stopped.emit()

            else:

                self.error.emit(
                    str(error)
                )

    # =========================================================
    # STATE
    # =========================================================

    @property
    def cancelled(self):

        return self._cancel_event.is_set()


class ChatController(QObject):

    response_chunk = Signal(str)

    response_ready = Signal(str)

    response_stopped = Signal()

    error_occurred = Signal(str)

    processing_started = Signal()

    processing_finished = Signal()

    def __init__(
        self,
        krish,
    ):

        super().__init__()

        self.krish = krish

        self._thread = None

        self._worker = None

        self._busy = False

        self._response = []

        self._stop_requested = False

    # =========================================================
    # STATE
    # =========================================================

    @property
    def busy(self):

        return self._busy

    @property
    def stopping(self):

        return self._stop_requested

    # =========================================================
    # SEND
    # =========================================================

    def send_message(
        self,
        message,
    ):

        message = message.strip()

        if not message:

            return False

        if self._busy:

            self.error_occurred.emit(
                "KRISH is still processing the previous request."
            )

            return False

        self._busy = True

        self._stop_requested = False

        self._response = []

        self.processing_started.emit()

        self._thread = QThread()

        self._worker = ChatWorker(
            self.krish,
            message,
        )

        self._worker.moveToThread(
            self._thread
        )

        # -----------------------------------------------------
        # Thread lifecycle
        # -----------------------------------------------------

        self._thread.started.connect(
            self._worker.run
        )

        # -----------------------------------------------------
        # Streaming
        # -----------------------------------------------------

        self._worker.chunk.connect(
            self._handle_chunk
        )

        # -----------------------------------------------------
        # Normal completion
        # -----------------------------------------------------

        self._worker.finished.connect(
            self._handle_finished
        )

        # -----------------------------------------------------
        # Cancellation
        # -----------------------------------------------------

        self._worker.stopped.connect(
            self._handle_stopped
        )

        # -----------------------------------------------------
        # Error
        # -----------------------------------------------------

        self._worker.error.connect(
            self._handle_error
        )

        # -----------------------------------------------------
        # Worker completion always stops the thread.
        # -----------------------------------------------------

        self._worker.finished.connect(
            self._thread.quit
        )

        self._worker.stopped.connect(
            self._thread.quit
        )

        self._worker.error.connect(
            self._thread.quit
        )

        self._thread.finished.connect(
            self._cleanup
        )

        self._thread.start()

        return True

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):

        if not self._busy:

            return False

        if self._stop_requested:

            return True

        self._stop_requested = True

        worker = self._worker

        if worker is not None:

            worker.cancel()

        return True

    # =========================================================
    # CHUNK
    # =========================================================

    def _handle_chunk(
        self,
        chunk,
    ):

        if self._stop_requested:

            return

        text = str(chunk)

        if not text:

            return

        self._response.append(
            text
        )

        self.response_chunk.emit(
            text
        )

    # =========================================================
    # FINISHED
    # =========================================================

    def _handle_finished(self):

        if self._stop_requested:

            self._handle_stopped()

            return

        response = "".join(
            self._response
        )

        self.response_ready.emit(
            response
        )

        self._busy = False

        self.processing_finished.emit()

    # =========================================================
    # STOPPED
    # =========================================================

    def _handle_stopped(self):

        if not self._busy:

            return

        self._stop_requested = True

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # Do NOT emit response_ready.
        #
        # The partial response already exists inside ChatView.
        # This prevents the stopped generation from being treated
        # as a completed response.
        # -----------------------------------------------------

        self.response_stopped.emit()

        self._busy = False

        self.processing_finished.emit()

    # =========================================================
    # ERROR
    # =========================================================

    def _handle_error(
        self,
        error,
    ):

        # -----------------------------------------------------
        # Cancellation is not an error.
        # -----------------------------------------------------

        if self._stop_requested:

            self._handle_stopped()

            return

        self.error_occurred.emit(
            str(error)
        )

        self._busy = False

        self.processing_finished.emit()

    # =========================================================
    # CLEANUP
    # =========================================================

    def _cleanup(self):

        worker = self._worker

        thread = self._thread

        self._worker = None

        self._thread = None

        if worker is not None:

            worker.deleteLater()

        if thread is not None:

            thread.deleteLater()