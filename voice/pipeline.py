class VoicePipeline:

    def __init__(
        self,
        stt=None,
        tts=None,
    ):

        self.stt = stt
        self.tts = tts

    def listen(self):

        if self.stt is None:
            raise RuntimeError(
                "STT backend not configured."
            )

        return self.stt.listen()

    def speak(self, text):

        if self.tts is None:
            raise RuntimeError(
                "TTS backend not configured."
            )

        return self.tts.speak(text)