from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
)


class KrishStatusBar(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("statusbar")

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            16, 6, 16, 6
        )

        layout.setSpacing(20)

        runtime = QLabel(
            "● Runtime"
        )

        runtime.setObjectName(
            "status_active"
        )

        security = QLabel(
            "● Security"
        )

        security.setObjectName(
            "status_active"
        )

        memory = QLabel(
            "● Memory"
        )

        memory.setObjectName(
            "status_active"
        )

        ai = QLabel(
            "● AI"
        )

        ai.setObjectName(
            "status_active"
        )

        layout.addWidget(runtime)
        layout.addWidget(security)
        layout.addWidget(memory)
        layout.addWidget(ai)

        layout.addStretch()