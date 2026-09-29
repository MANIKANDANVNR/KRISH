from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
)


def read_value(obj, names, default="Unavailable"):

    for name in names:

        try:

            value = getattr(obj, name)

            if callable(value):
                value = value()

            if value is not None:
                return str(value)

        except Exception:
            continue

    return default


class DashboardPanel(QWidget):

    def __init__(self, krish):

        super().__init__()

        self.krish = krish

        self._build()

    def _build(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(18)

        title = QLabel("KRISH SYSTEM DASHBOARD")
        title.setObjectName("panel_title")

        description = QLabel(
            "Live overview of the KRISH runtime, brain, memory and security subsystems."
        )

        description.setObjectName("panel_description")
        description.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)

        cards = QHBoxLayout()
        cards.setSpacing(14)

        self.runtime_card = self._card(
            "RUNTIME",
            "Loading...",
            "Core runtime state",
        )

        self.brain_card = self._card(
            "BRAIN",
            "Loading...",
            "AI provider status",
        )

        self.memory_card = self._card(
            "MEMORY",
            "Loading...",
            "Persistent intelligence",
        )

        self.security_card = self._card(
            "SECURITY",
            "Loading...",
            "Protection state",
        )

        cards.addWidget(self.runtime_card)
        cards.addWidget(self.brain_card)
        cards.addWidget(self.memory_card)
        cards.addWidget(self.security_card)

        layout.addLayout(cards)

        system = QFrame()
        system.setObjectName("card")

        system_layout = QVBoxLayout(system)

        heading = QLabel("SYSTEM INFORMATION")
        heading.setObjectName("card_title")

        self.info = QLabel()
        self.info.setWordWrap(True)

        system_layout.addWidget(heading)
        system_layout.addWidget(self.info)

        layout.addWidget(system)

        refresh = QPushButton("Refresh")
        refresh.setObjectName("primary")
        refresh.clicked.connect(self.refresh)

        layout.addWidget(refresh)
        layout.addStretch()

        self.refresh()

    def _card(self, title, value, description):

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setObjectName("card_title")

        value_label = QLabel(value)
        value_label.setObjectName("card_value")

        description_label = QLabel(description)
        description_label.setObjectName("card_description")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(description_label)

        card.value_label = value_label

        return card

    def refresh(self):

        runtime = getattr(self.krish, "runtime", None)
        brain = getattr(self.krish, "brain", None)
        memory = getattr(self.krish, "memory", None)
        security = getattr(self.krish, "security", None)

        self.runtime_card.value_label.setText(
            read_value(
                runtime,
                ["state", "status", "mode"],
                "READY",
            )
        )

        self.brain_card.value_label.setText(
            read_value(
                brain,
                ["status", "provider", "model"],
                "READY",
            )
        )

        self.memory_card.value_label.setText(
            "ACTIVE" if memory else "UNAVAILABLE"
        )

        self.security_card.value_label.setText(
            "ACTIVE" if security else "UNAVAILABLE"
        )

        self.info.setText(
            f"KRISH object: {type(self.krish).__name__}\n"
            f"Runtime: {type(runtime).__name__ if runtime else 'Unavailable'}\n"
            f"Brain: {type(brain).__name__ if brain else 'Unavailable'}\n"
            f"Memory: {type(memory).__name__ if memory else 'Unavailable'}\n"
            f"Security: {type(security).__name__ if security else 'Unavailable'}"
        )