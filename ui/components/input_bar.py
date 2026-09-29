from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class InputBar(QFrame):

    message_sent = Signal(str)
    voice_requested = Signal()
    stop_requested = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName(
            "input_bar"
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            18,
            10,
            18,
            14,
        )

        layout.setSpacing(8)

        # =====================================================
        # INPUT
        # =====================================================

        self.input = QLineEdit()

        self.input.setObjectName(
            "input"
        )

        self.input.setPlaceholderText(
            "Message KRISH..."
        )

        self.input.setClearButtonEnabled(
            True
        )

        self.input.returnPressed.connect(
            self._send
        )

        # =====================================================
        # VOICE
        # =====================================================

        self.voice_button = QPushButton(
            "🎙"
        )

        self.voice_button.setObjectName(
            "voice"
        )

        self.voice_button.setToolTip(
            "Voice input"
        )

        self.voice_button.clicked.connect(
            self.voice_requested.emit
        )

        # =====================================================
        # STOP
        # =====================================================

        self.stop_button = QPushButton(
            "Stop"
        )

        self.stop_button.setObjectName(
            "stop"
        )

        self.stop_button.setToolTip(
            "Stop KRISH response"
        )

        self.stop_button.setVisible(
            False
        )

        self.stop_button.clicked.connect(
            self._stop
        )

        # =====================================================
        # SEND
        # =====================================================

        self.send_button = QPushButton(
            "Send"
        )

        self.send_button.setObjectName(
            "send"
        )

        self.send_button.setToolTip(
            "Send message"
        )

        self.send_button.clicked.connect(
            self._send
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        layout.addWidget(
            self.input,
            1,
        )

        layout.addWidget(
            self.voice_button
        )

        layout.addWidget(
            self.stop_button
        )

        layout.addWidget(
            self.send_button
        )

    # =========================================================
    # SEND
    # =========================================================

    def _send(self):

        if not self.input.isEnabled():
            return

        text = self.input.text().strip()

        if not text:
            return

        self.input.clear()

        self.message_sent.emit(
            text
        )

    # =========================================================
    # STOP
    # =========================================================

    def _stop(self):

        if not self.stop_button.isVisible():
            return

        self.stop_requested.emit()

    # =========================================================
    # PUBLIC UI STATE
    # =========================================================

    def set_processing(
        self,
        processing,
    ):

        processing = bool(
            processing
        )

        self.input.setEnabled(
            not processing
        )

        self.send_button.setVisible(
            not processing
        )

        self.stop_button.setVisible(
            processing
        )

        self.voice_button.setEnabled(
            not processing
        )

        if not processing:

            self.input.setFocus()

    def focus_input(self):

        self.input.setFocus()