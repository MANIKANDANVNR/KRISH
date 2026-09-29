from PySide6.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QWidget, QApplication
from ui.components.message_bubble import MessageBubble


class ChatView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chat_area")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self.container = QWidget()
        self.messages_layout = QVBoxLayout(self.container)
        self.messages_layout.setContentsMargins(24, 24, 24, 24)
        self.messages_layout.setSpacing(14)
        self.messages_layout.addStretch()
        self.scroll.setWidget(self.container)
        outer.addWidget(self.scroll)
        self.current_assistant = None

    def clear(self):
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.current_assistant = None

    def add_message(self, sender, message):
        bubble = MessageBubble(sender, message)
        bubble.copy_requested.connect(self._copy)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)
        self._scroll_bottom()
        return bubble

    def begin_stream(self):
        self.current_assistant = self.add_message("KRISH", "")
        return self.current_assistant

    def append_stream(self, chunk):
        if self.current_assistant is None:
            self.begin_stream()
        self.current_assistant.set_message(self.current_assistant.message + chunk)
        self._scroll_bottom()

    def finish_stream(self):
        self.current_assistant = None

    def load_messages(self, messages):
        self.clear()
        for message in messages:
            self.add_message(message["role"].upper(), message["content"])

    def _scroll_bottom(self):
        bar = self.scroll.verticalScrollBar()
        bar.setValue(bar.maximum())

    @staticmethod
    def _copy(text):
        QApplication.clipboard().setText(text)
