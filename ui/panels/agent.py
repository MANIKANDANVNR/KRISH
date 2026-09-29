from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QPushButton,
)


class AgentPanel(QWidget):

    def __init__(self, krish):

        super().__init__()

        self.krish = krish

        self._build()

    def _build(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(18)

        title = QLabel("AGENT")
        title.setObjectName("panel_title")

        description = QLabel(
            "Planning, execution, verification and recovery architecture."
        )

        description.setObjectName("panel_description")
        description.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)

        grid = QGridLayout()
        grid.setSpacing(14)

        components = [
            ("INTELLIGENT AGENT", "intelligent_agent"),
            ("PLANNER", "planner"),
            ("EXECUTOR", "executor"),
            ("VERIFIER", "verifier"),
            ("RECOVERY", "recovery"),
            ("REPORTER", "reporter"),
            ("TASK", "task"),
            ("INTENT", "intent"),
        ]

        for index, (name, attribute) in enumerate(components):

            card = self._component_card(
                name,
                attribute,
            )

            grid.addWidget(
                card,
                index // 2,
                index % 2,
            )

        layout.addLayout(grid)

        refresh = QPushButton("Refresh Agent State")
        refresh.setObjectName("primary")
        refresh.clicked.connect(self.refresh)

        layout.addWidget(refresh)
        layout.addStretch()

        self.refresh()

    def _component_card(self, name, attribute):

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        title = QLabel(name)
        title.setObjectName("card_title")

        value = QLabel("Loading...")
        value.setObjectName("card_value")

        layout.addWidget(title)
        layout.addWidget(value)

        card.attribute = attribute
        card.value = value

        return card

    def refresh(self):

        agent = getattr(
            self.krish,
            "agent",
            None,
        )

        for i in range(
            self.findChildren(QFrame).__len__()
        ):

            pass

        for card in self.findChildren(QFrame):

            attribute = getattr(
                card,
                "attribute",
                None,
            )

            value_label = getattr(
                card,
                "value",
                None,
            )

            if not attribute or value_label is None:
                continue

            component = None

            if agent is not None:

                component = getattr(
                    agent,
                    attribute,
                    None,
                )

            if component is not None:

                value_label.setText(
                    f"ACTIVE\n{type(component).__name__}"
                )

            else:

                value_label.setText(
                    "AVAILABLE"
                )