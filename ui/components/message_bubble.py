from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MessageBubble(QFrame):
    copy_requested = Signal(str)

    def __init__(self, sender: str, message: str, parent=None):
        super().__init__(parent)

        self.sender = sender
        self.message = message

        self.setObjectName("messageBubble")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        self.sender_label = QLabel(sender)
        self.sender_label.setObjectName("messageSender")

        self.message_label = QLabel(message)
        self.message_label.setObjectName("messageText")
        self.message_label.setWordWrap(True)
        self.message_label.setTextFormat(Qt.TextFormat.PlainText)

        # PySide6 6.11+ requires using the Qt enum instead of
        # combining TextInteractionFlag with a raw integer.
        self.message_label.setTextInteractionFlags(
            self.message_label.textInteractionFlags()
            | Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout.addWidget(self.sender_label)
        layout.addWidget(self.message_label)

        # Emit the message when the user requests a copy operation.
        self.message_label.mousePressEvent = self._mouse_press_event

    def _mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.copy_requested.emit(self.message)

        QLabel.mousePressEvent(self.message_label, event)
