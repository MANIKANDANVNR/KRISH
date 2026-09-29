from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QScrollArea,
)


class SecurityPanel(QWidget):

    def __init__(self, krish):

        super().__init__()

        self.krish = krish

        self.capability_labels = {}

        self._build()

        self.refresh()

    # =========================================================
    # BUILD
    # =========================================================

    def _build(self):

        outer = QVBoxLayout(self)

        outer.setContentsMargins(
            32,
            28,
            32,
            28,
        )

        outer.setSpacing(16)

        title = QLabel("SECURITY")
        title.setObjectName("panel_title")

        description = QLabel(
            "Owner authentication, authorization, permissions, "
            "capabilities and protection status."
        )

        description.setObjectName(
            "panel_description"
        )

        description.setWordWrap(True)

        outer.addWidget(title)
        outer.addWidget(description)

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)
        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        content = QWidget()

        layout = QVBoxLayout(content)

        layout.setContentsMargins(
            0,
            0,
            8,
            20,
        )

        layout.setSpacing(14)

        # =====================================================
        # SECURITY CORE
        # =====================================================

        subsystem = self._create_card()

        subsystem_layout = subsystem.layout()

        heading = QLabel(
            "SECURITY CORE"
        )

        heading.setObjectName(
            "card_title"
        )

        self.status = QLabel(
            "CHECKING"
        )

        self.status.setObjectName(
            "card_value"
        )

        self.details = QLabel()

        self.details.setWordWrap(True)

        subsystem_layout.addWidget(
            heading
        )

        subsystem_layout.addWidget(
            self.status
        )

        subsystem_layout.addWidget(
            self.details
        )

        layout.addWidget(
            subsystem
        )

        # =====================================================
        # SESSION
        # =====================================================

        session_card = self._create_card()

        session_layout = session_card.layout()

        heading = QLabel(
            "OWNER SESSION"
        )

        heading.setObjectName(
            "card_title"
        )

        session_layout.addWidget(
            heading
        )

        self.authentication_value = QLabel(
            "UNKNOWN"
        )

        self.session_value = QLabel(
            "UNKNOWN"
        )

        self.session_id_value = QLabel(
            "NOT EXPOSED"
        )

        self.lockdown_value = QLabel(
            "UNKNOWN"
        )

        self._add_component_row(
            session_layout,
            "Authentication",
            self.authentication_value,
        )

        self._add_component_row(
            session_layout,
            "Session",
            self.session_value,
        )

        self._add_component_row(
            session_layout,
            "Session ID",
            self.session_id_value,
        )

        self._add_component_row(
            session_layout,
            "Lockdown",
            self.lockdown_value,
        )

        layout.addWidget(
            session_card
        )

        # =====================================================
        # CAPABILITIES
        # =====================================================

        capability_card = self._create_card()

        capability_layout = capability_card.layout()

        heading = QLabel(
            "LIVE CAPABILITY STATE"
        )

        heading.setObjectName(
            "card_title"
        )

        capability_layout.addWidget(
            heading
        )

        capability_names = [
            (
                "internet",
                "Internet Access",
            ),
            (
                "web_search",
                "Web Search",
            ),
            (
                "external_data",
                "External Data",
            ),
            (
                "file_access",
                "File Access",
            ),
            (
                "system_access",
                "System Access",
            ),
            (
                "application_launch",
                "Application Launch",
            ),
            (
                "python_terminal",
                "Python / Terminal",
            ),
            (
                "voice_input",
                "Voice Input",
            ),
            (
                "voice_output",
                "Voice Output",
            ),
            (
                "automatic_evolution",
                "Automatic Evolution",
            ),
        ]

        for name, title in capability_names:

            self._add_capability_status(
                capability_layout,
                name,
                title,
            )

        layout.addWidget(
            capability_card
        )

        # =====================================================
        # SECURITY COMPONENTS
        # =====================================================

        components = self._create_card()

        component_layout = components.layout()

        heading = QLabel(
            "SECURITY COMPONENTS"
        )

        heading.setObjectName(
            "card_title"
        )

        component_layout.addWidget(
            heading
        )

        self.authorization_value = QLabel()
        self.permissions_value = QLabel()
        self.policy_value = QLabel()
        self.audit_value = QLabel()
        self.identity_value = QLabel()

        values = [
            (
                "Authorization",
                self.authorization_value,
            ),
            (
                "Permissions",
                self.permissions_value,
            ),
            (
                "Policy",
                self.policy_value,
            ),
            (
                "Audit",
                self.audit_value,
            ),
            (
                "Identity",
                self.identity_value,
            ),
        ]

        for name, value in values:

            self._add_component_row(
                component_layout,
                name,
                value,
            )

        layout.addWidget(
            components
        )

        # =====================================================
        # ACCESS MODEL
        # =====================================================

        access = self._create_card()

        access_layout = access.layout()

        heading = QLabel(
            "ACCESS MODEL"
        )

        heading.setObjectName(
            "card_title"
        )

        explanation = QLabel(
            "KRISH follows a deny by default security model. "
            "A UI switch never grants authority by itself. "
            "Capability activation must pass authentication, "
            "session validation, permissions, authorization, "
            "risk policy and approval requirements."
        )

        explanation.setWordWrap(True)

        access_layout.addWidget(
            heading
        )

        access_layout.addWidget(
            explanation
        )

        layout.addWidget(
            access
        )

        # =====================================================
        # EVOLUTION
        # =====================================================

        evolution = self._create_card()

        evolution_layout = evolution.layout()

        heading = QLabel(
            "EVOLUTION PROTECTION"
        )

        heading.setObjectName(
            "card_title"
        )

        evolution_status = QLabel(
            "AUTOMATIC EVOLUTION: OFF"
        )

        evolution_status.setObjectName(
            "capability_off"
        )

        evolution_description = QLabel(
            "KRISH cannot autonomously modify its own security, "
            "permissions, architecture or behavior. "
            "Evolution requires explicit owner authorization "
            "for a specific component or action."
        )

        evolution_description.setWordWrap(True)

        evolution_layout.addWidget(
            heading
        )

        evolution_layout.addWidget(
            evolution_status
        )

        evolution_layout.addWidget(
            evolution_description
        )

        layout.addWidget(
            evolution
        )

        # =====================================================
        # ACTIONS
        # =====================================================

        actions = QHBoxLayout()

        refresh = QPushButton(
            "Refresh Security State"
        )

        refresh.setObjectName(
            "primary"
        )

        refresh.clicked.connect(
            self.refresh
        )

        actions.addWidget(
            refresh
        )

        actions.addStretch()

        layout.addLayout(
            actions
        )

        self.warning = QLabel()

        self.warning.setWordWrap(True)

        self.warning.setObjectName(
            "panel_description"
        )

        layout.addWidget(
            self.warning
        )

        layout.addStretch()

        scroll.setWidget(
            content
        )

        outer.addWidget(
            scroll,
            1,
        )

    # =========================================================
    # HELPERS
    # =========================================================

    def _create_card(self):

        card = QFrame()

        card.setObjectName(
            "card"
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(10)

        return card

    def _add_capability_status(
        self,
        layout,
        name,
        title,
    ):

        row = QHBoxLayout()

        label = QLabel(title)

        label.setObjectName(
            "settings_item_title"
        )

        value = QLabel("OFF")

        value.setObjectName(
            "capability_off"
        )

        row.addWidget(label)
        row.addStretch()
        row.addWidget(value)

        layout.addLayout(row)

        self.capability_labels[name] = value

    def _add_component_row(
        self,
        layout,
        name,
        value,
    ):

        row = QHBoxLayout()

        label = QLabel(name)

        label.setObjectName(
            "settings_item_title"
        )

        value.setObjectName(
            "capability_off"
        )

        value.setText(
            "NOT EXPOSED"
        )

        row.addWidget(label)
        row.addStretch()
        row.addWidget(value)

        layout.addLayout(row)

    @staticmethod
    def _repolish(widget):

        style = widget.style()

        style.unpolish(widget)
        style.polish(widget)

        widget.update()

    # =========================================================
    # SECURITY
    # =========================================================

    def _get_security(self):

        security = getattr(
            self.krish,
            "security",
            None,
        )

        if security is not None:
            return security

        return getattr(
            self.krish,
            "_security",
            None,
        )

    def _get_runtime(self):

        runtime = getattr(
            self.krish,
            "runtime",
            None,
        )

        if runtime is not None:
            return runtime

        return getattr(
            self.krish,
            "_runtime",
            None,
        )

    # =========================================================
    # CAPABILITIES
    # =========================================================

    def _read_capabilities(self):

        security = self._get_security()

        if security is not None:

            getter = getattr(
                security,
                "capabilities",
                None,
            )

            if callable(getter):

                try:

                    value = getter()

                    if isinstance(
                        value,
                        dict,
                    ):
                        return dict(value)

                except Exception:
                    pass

            value = getattr(
                security,
                "_capabilities",
                None,
            )

            if isinstance(
                value,
                dict,
            ):
                return dict(value)

        runtime = self._get_runtime()

        if runtime is not None:

            capabilities = getattr(
                runtime,
                "capabilities",
                None,
            )

            if callable(capabilities):

                try:
                    capabilities = capabilities()
                except Exception:
                    capabilities = None

            if isinstance(
                capabilities,
                dict,
            ):
                return dict(capabilities)

        return {}

    # =========================================================
    # COMPONENT STATE
    # =========================================================

    def _component_state(
        self,
        security,
        name,
    ):

        if security is None:
            return "NOT EXPOSED"

        value = getattr(
            security,
            name,
            None,
        )

        if value is None:
            return "NOT EXPOSED"

        if isinstance(
            value,
            bool,
        ):

            return (
                "ACTIVE"
                if value
                else "INACTIVE"
            )

        return type(value).__name__

    def _set_state_style(
        self,
        label,
        state,
    ):

        label.setText(state)

        if state in (
            "ACTIVE",
            "ON",
            "Authenticated",
            "Active",
            "Normal",
        ):

            label.setObjectName(
                "capability_on"
            )

        else:

            label.setObjectName(
                "capability_off"
            )

        self._repolish(label)

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        security = self._get_security()

        runtime = self._get_runtime()

        # -----------------------------------------------------
        # CORE SECURITY
        # -----------------------------------------------------

        if security is None:

            self.status.setText(
                "SECURITY PROTECTED"
            )

            self.details.setText(
                "The SecurityKernel is not directly exposed "
                "through the current application object."
            )

        else:

            self.status.setText(
                "ACTIVE"
            )

            authentication = getattr(
                security,
                "authentication",
                None,
            )

            authorization = getattr(
                security,
                "authorization",
                None,
            )

            policy = getattr(
                security,
                "policy",
                None,
            )

            lockdown = getattr(
                security,
                "lockdown",
                None,
            )

            lines = [
                f"Kernel: {type(security).__name__}",
                (
                    "Authentication: "
                    f"{type(authentication).__name__}"
                    if authentication is not None
                    else "Authentication: ACTIVE"
                ),
                (
                    "Authorization: "
                    f"{type(authorization).__name__}"
                    if authorization is not None
                    else "Authorization: ACTIVE"
                ),
                (
                    "Policy: "
                    f"{type(policy).__name__}"
                    if policy is not None
                    else "Policy: ACTIVE"
                ),
                (
                    "Lockdown: "
                    f"{type(lockdown).__name__}"
                    if lockdown is not None
                    else "Lockdown: ACTIVE"
                ),
            ]

            self.details.setText(
                "\n".join(lines)
            )

        # -----------------------------------------------------
        # AUTHENTICATION
        # -----------------------------------------------------

        authenticated = False

        if security is not None:

            authentication = getattr(
                security,
                "authentication",
                None,
            )

            if authentication is not None:

                authenticated = bool(
                    getattr(
                        authentication,
                        "authenticated",
                        False,
                    )
                )

        self._set_state_style(
            self.authentication_value,
            (
                "Authenticated"
                if authenticated
                else "Not authenticated"
            ),
        )

        # -----------------------------------------------------
        # SESSION
        # -----------------------------------------------------

        session_id = None

        if security is not None:

            getter = getattr(
                security,
                "get_active_session_id",
                None,
            )

            if callable(getter):

                try:
                    session_id = getter()
                except Exception:
                    session_id = None

        self._set_state_style(
            self.session_value,
            (
                "Active"
                if session_id
                else "No active session"
            ),
        )

        if session_id:

            # Do not expose the complete session identifier
            # in the UI.
            session_text = str(session_id)

            if len(session_text) > 12:

                session_text = (
                    session_text[:8]
                    + "..."
                    + session_text[-4:]
                )

            self.session_id_value.setText(
                session_text
            )

            self.session_id_value.setObjectName(
                "capability_on"
            )

        else:

            self.session_id_value.setText(
                "NOT EXPOSED"
            )

            self.session_id_value.setObjectName(
                "capability_off"
            )

        self._repolish(
            self.session_id_value
        )

        # -----------------------------------------------------
        # LOCKDOWN
        # -----------------------------------------------------

        lockdown_active = False

        if security is not None:

            lockdown = getattr(
                security,
                "lockdown",
                None,
            )

            if lockdown is not None:

                lockdown_active = bool(
                    getattr(
                        lockdown,
                        "engaged",
                        False,
                    )
                )

        self._set_state_style(
            self.lockdown_value,
            (
                "LOCKDOWN"
                if lockdown_active
                else "Normal"
            ),
        )

        # -----------------------------------------------------
        # SECURITY COMPONENTS
        # -----------------------------------------------------

        component_names = [
            (
                "authorization",
                self.authorization_value,
            ),
            (
                "permissions",
                self.permissions_value,
            ),
            (
                "policy",
                self.policy_value,
            ),
            (
                "audit",
                self.audit_value,
            ),
            (
                "identity",
                self.identity_value,
            ),
        ]

        for name, label in component_names:

            state = self._component_state(
                security,
                name,
            )

            if state not in (
                "NOT EXPOSED",
                "INACTIVE",
            ):

                state = "ACTIVE"

            self._set_state_style(
                label,
                state,
            )

        # -----------------------------------------------------
        # CAPABILITIES
        # -----------------------------------------------------

        capabilities = (
            self._read_capabilities()
        )

        for name, label in (
            self.capability_labels.items()
        ):

            enabled = bool(
                capabilities.get(
                    name,
                    False,
                )
            )

            # Automatic evolution is never allowed
            # to become active.
            if name == "automatic_evolution":
                enabled = False

            self._set_state_style(
                label,
                "ON" if enabled else "OFF",
            )

        # -----------------------------------------------------
        # WARNING / MODEL
        # -----------------------------------------------------

        if lockdown_active:

            self.warning.setText(
                "SECURITY LOCKDOWN IS ACTIVE. "
                "All protected capabilities must remain disabled "
                "until the security subsystem explicitly releases "
                "lockdown."
            )

            self.warning.setObjectName(
                "status_warning"
            )

        elif runtime is None:

            self.warning.setText(
                "Runtime state is unavailable. "
                "Security remains deny by default."
            )

            self.warning.setObjectName(
                "panel_description"
            )

        else:

            self.warning.setText(
                "Security enforcement is independent of the UI. "
                "Changing a visual switch cannot bypass authentication, "
                "authorization, permissions, policy or approval requirements."
            )

            self.warning.setObjectName(
                "panel_description"
            )

        self._repolish(
            self.warning
        )