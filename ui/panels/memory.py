from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)


class MemoryPanel(QWidget):

    def __init__(self, krish):

        super().__init__()

        self.krish = krish

        self._build()

    def _build(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(14)

        title = QLabel("MEMORY")
        title.setObjectName("panel_title")

        description = QLabel(
            "Conversation memory and persistent intelligence available to KRISH."
        )

        description.setObjectName("panel_description")
        description.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(
            ["Role", "Content"]
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table, 1)

        refresh = QPushButton("Refresh Memory")
        refresh.setObjectName("primary")
        refresh.clicked.connect(self.refresh)

        layout.addWidget(refresh)

        self.refresh()

    def refresh(self):

        self.table.setRowCount(0)

        try:

            memory = self.krish.memory
            conversation = memory.conversation

            messages = conversation.recent(1000)

        except Exception as exc:

            self._error(str(exc))
            return

        for message in messages:

            if isinstance(message, dict):

                role = message.get(
                    "role",
                    message.get("sender", "UNKNOWN"),
                )

                content = message.get(
                    "content",
                    message.get("message", ""),
                )

            else:

                role = getattr(
                    message,
                    "role",
                    "UNKNOWN",
                )

                content = getattr(
                    message,
                    "content",
                    str(message),
                )

            row = self.table.rowCount()

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(role)),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(str(content)),
            )

    def _error(self, message):

        self.table.setRowCount(1)

        self.table.setItem(
            0,
            0,
            QTableWidgetItem("ERROR"),
        )

        self.table.setItem(
            0,
            1,
            QTableWidgetItem(message),
        )