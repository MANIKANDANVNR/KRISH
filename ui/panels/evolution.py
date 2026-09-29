from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QPlainTextEdit,
)


class EvolutionPanel(QWidget):

    def __init__(self, krish):

        super().__init__()

        self.krish = krish

        self._build()

    def _build(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        title = QLabel("EVOLUTION")
        title.setObjectName("panel_title")

        description = QLabel(
            "Owner controlled evolution. KRISH does not modify itself automatically."
        )

        description.setObjectName("panel_description")
        description.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)

        state = QFrame()
        state.setObjectName("card")

        state_layout = QVBoxLayout(state)

        heading = QLabel("EVOLUTION CONTROL")
        heading.setObjectName("card_title")

        status = QLabel(
            "MANUAL CONTROL ONLY"
        )
        status.setObjectName("card_value")

        explanation = QLabel(
            "Evolution operations must be explicitly initiated and authorized "
            "by the owner. Opening this page does not trigger an improvement."
        )

        explanation.setWordWrap(True)

        state_layout.addWidget(heading)
        state_layout.addWidget(status)
        state_layout.addWidget(explanation)

        layout.addWidget(state)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.log, 1)

        refresh = QPushButton("Inspect Evolution System")
        refresh.setObjectName("primary")
        refresh.clicked.connect(self.refresh)

        layout.addWidget(refresh)

        self.refresh()

    def refresh(self):

        evolution = getattr(
            self.krish,
            "evolution",
            None,
        )

        if evolution is None:

            self.log.setPlainText(
                "Evolution subsystem is not currently exposed "
                "through the KRISH runtime.\n\n"
                "No automatic evolution operation has been performed."
            )

            return

        lines = [
            f"Subsystem: {type(evolution).__name__}",
            "",
            "Available components:",
        ]

        for name in dir(evolution):

            if name.startswith("_"):
                continue

            try:

                value = getattr(
                    evolution,
                    name,
                )

                if callable(value):
                    continue

                lines.append(
                    f"  • {name}: {type(value).__name__}"
                )

            except Exception:
                continue

        lines.append("")
        lines.append(
            "No evolution operation was executed."
        )

        self.log.setPlainText(
            "\n".join(lines)
        )