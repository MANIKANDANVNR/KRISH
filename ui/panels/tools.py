from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)


class ToolsPanel(QWidget):

    def __init__(self, krish):

        super().__init__()

        self.krish = krish

        self._build()

    def _build(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(14)

        title = QLabel("TOOLS")
        title.setObjectName("panel_title")

        description = QLabel(
            "Registered KRISH tools and their current runtime availability."
        )

        description.setObjectName("panel_description")
        description.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)

        self.table = QTableWidget()
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(
            ["Tool", "Type", "State"]
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table, 1)

        refresh = QPushButton("Refresh Tools")
        refresh.setObjectName("primary")
        refresh.clicked.connect(self.refresh)

        layout.addWidget(refresh)

        self.refresh()

    def refresh(self):

        self.table.setRowCount(0)

        registry = getattr(
            self.krish,
            "tools",
            None,
        )

        if registry is None:

            registry = getattr(
                self.krish,
                "tool_registry",
                None,
            )

        if registry is None:

            self._add(
                "Tool Registry",
                "Unavailable",
                "NOT EXPOSED",
            )

            return

        names = []

        for attribute in (
            "tools",
            "registry",
            "_tools",
            "registered_tools",
        ):

            value = getattr(
                registry,
                attribute,
                None,
            )

            if isinstance(value, dict):

                names = list(value.keys())
                break

        if not names:

            try:

                names = list(
                    registry.list_tools()
                )

            except Exception:
                pass

        if not names:

            self._add(
                "Tool Registry",
                type(registry).__name__,
                "ACTIVE",
            )

            return

        for name in names:

            tool = None

            try:

                tool = (
                    registry.tools.get(name)
                    if hasattr(registry, "tools")
                    and isinstance(registry.tools, dict)
                    else None
                )

            except Exception:
                pass

            self._add(
                str(name),
                type(tool).__name__
                if tool
                else "Tool",
                "REGISTERED",
            )

    def _add(self, name, tool_type, state):

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(name),
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(tool_type),
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(state),
        )