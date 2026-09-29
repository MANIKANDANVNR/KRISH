from PySide6.QtCore import Signal, QSettings, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QComboBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QApplication,
    QMessageBox,
)

from ui.theme import (
    THEME_DARK,
    THEME_LIGHT,
    THEME_SYSTEM,
    apply_theme,
)


class CapabilitySwitch(QPushButton):
    changed = Signal(bool)

    def __init__(
        self,
        name,
        title,
        description,
        parent=None,
    ):
        super().__init__(parent)

        self.name = name
        self.title = title
        self.description = description

        self._value = False
        self._updating = False

        self.setCheckable(True)

        self.clicked.connect(
            self._clicked
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )

        self._update_visual()

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        self._updating = True

        try:
            self._value = bool(value)
            self.setChecked(self._value)
            self._update_visual()

        finally:
            self._updating = False

    def _clicked(self, checked):

        if self._updating:
            return

        requested = bool(checked)

        # The visual state is NOT considered authoritative.
        # SettingsPanel asks SecurityKernel first.
        self.changed.emit(requested)

    def _update_visual(self):

        self.setChecked(
            self._value
        )

        if self._value:
            self.setObjectName(
                "switch_on"
            )
            self.setText("ON")

        else:
            self.setObjectName(
                "switch_off"
            )
            self.setText("OFF")

        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class SettingsPanel(QWidget):

    def __init__(self, krish):
        super().__init__()

        self.krish = krish

        self.settings = QSettings(
            "KRISH",
            "PersonalAI",
        )

        self.capability_switches = {}

        self._building = True

        self._build()

        self._building = False

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

        outer.setSpacing(18)

        title = QLabel(
            "SETTINGS"
        )

        title.setObjectName(
            "panel_title"
        )

        description = QLabel(
            "Control KRISH appearance, capabilities and runtime preferences."
        )

        description.setObjectName(
            "panel_description"
        )

        description.setWordWrap(True)

        outer.addWidget(title)
        outer.addWidget(description)

        # =====================================================
        # SCROLL
        # =====================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        content = QWidget()

        layout = QVBoxLayout(
            content
        )

        layout.setContentsMargins(
            0,
            0,
            8,
            20,
        )

        layout.setSpacing(14)

        # =====================================================
        # APPEARANCE
        # =====================================================

        appearance = self._create_section(
            "Appearance",
            "Choose how the KRISH interface should look.",
        )

        appearance_layout = (
            appearance.layout()
        )

        row = QHBoxLayout()

        labels = QVBoxLayout()

        title_label = QLabel(
            "Theme"
        )

        title_label.setObjectName(
            "settings_item_title"
        )

        description_label = QLabel(
            "Dark, Light, or follow the Windows system appearance."
        )

        description_label.setObjectName(
            "settings_item_description"
        )

        labels.addWidget(
            title_label
        )

        labels.addWidget(
            description_label
        )

        self.theme_combo = QComboBox()

        self.theme_combo.addItem(
            "Dark",
            THEME_DARK,
        )

        self.theme_combo.addItem(
            "Light",
            THEME_LIGHT,
        )

        self.theme_combo.addItem(
            "System",
            THEME_SYSTEM,
        )

        self.theme_combo.currentIndexChanged.connect(
            self._theme_changed
        )

        row.addLayout(
            labels,
            1
        )

        row.addWidget(
            self.theme_combo
        )

        appearance_layout.addLayout(
            row
        )

        layout.addWidget(
            appearance
        )

        # =====================================================
        # INTERNET
        # =====================================================

        internet = self._create_section(
            "Internet",
            "Network and external data capabilities remain disabled by default.",
        )

        internet_layout = (
            internet.layout()
        )

        self._add_capability(
            internet_layout,
            "internet",
            "Internet Access",
            "Allow KRISH network access after explicit owner authorization.",
        )

        self._add_capability(
            internet_layout,
            "web_search",
            "Web Search",
            "Allow KRISH to perform web searches after explicit owner authorization.",
        )

        self._add_capability(
            internet_layout,
            "external_data",
            "External Data",
            "Allow retrieval from configured external data sources after explicit owner authorization.",
        )

        layout.addWidget(
            internet
        )

        # =====================================================
        # FILE ACCESS
        # =====================================================

        file_section = self._create_section(
            "File Access",
            "File access is independently controlled and remains OFF by default.",
        )

        file_layout = (
            file_section.layout()
        )

        self._add_capability(
            file_layout,
            "file_access",
            "File Access",
            "Allow KRISH to access explicitly permitted files and paths.",
        )

        self._add_information_row(
            file_layout,
            "Allowed Paths",
            "Managed by the security and permission subsystem.",
        )

        self._add_information_row(
            file_layout,
            "Granted Files",
            "Only explicitly granted resources should be accessible.",
        )

        layout.addWidget(
            file_section
        )

        # =====================================================
        # SYSTEM
        # =====================================================

        system = self._create_section(
            "System Access",
            "Operating system capabilities require separate authorization.",
        )

        system_layout = (
            system.layout()
        )

        self._add_capability(
            system_layout,
            "system_access",
            "System Access",
            "Allow controlled system operations.",
        )

        self._add_capability(
            system_layout,
            "application_launch",
            "Application Launch",
            "Allow launching applications after authorization.",
        )

        self._add_capability(
            system_layout,
            "python_terminal",
            "Python / Terminal",
            "Allow controlled code or terminal operations.",
        )

        layout.addWidget(
            system
        )

        # =====================================================
        # VOICE
        # =====================================================

        voice = self._create_section(
            "Voice",
            "Voice input and output are independently controlled.",
        )

        voice_layout = (
            voice.layout()
        )

        self._add_capability(
            voice_layout,
            "voice_input",
            "Voice Input",
            "Allow microphone and speech input after explicit owner authorization.",
        )

        self._add_capability(
            voice_layout,
            "voice_output",
            "Voice Output",
            "Allow KRISH speech output after explicit owner authorization.",
        )

        layout.addWidget(
            voice
        )

        # =====================================================
        # AI
        # =====================================================

        ai = self._create_section(
            "AI",
            "Current provider and model configuration.",
        )

        ai_layout = (
            ai.layout()
        )

        self.provider_value = QLabel(
            "Detecting..."
        )

        self.provider_value.setObjectName(
            "settings_item_title"
        )

        self.model_value = QLabel(
            "Detecting..."
        )

        self.model_value.setObjectName(
            "settings_item_title"
        )

        self._add_readonly_row(
            ai_layout,
            "Provider",
            self.provider_value,
        )

        self._add_readonly_row(
            ai_layout,
            "Model",
            self.model_value,
        )

        self._add_information_row(
            ai_layout,
            "Response Mode",
            "Streaming responses are used by the chat controller when supported.",
        )

        layout.addWidget(
            ai
        )

        # =====================================================
        # SECURITY
        # =====================================================

        security = self._create_section(
            "Security",
            "Security controls remain enforced outside the user interface.",
        )

        security_layout = (
            security.layout()
        )

        self.authentication_value = QLabel(
            "Checking..."
        )

        self.session_value = QLabel(
            "Checking..."
        )

        self.lockdown_value = QLabel(
            "Checking..."
        )

        self.authentication_value.setObjectName(
            "settings_item_title"
        )

        self.session_value.setObjectName(
            "settings_item_title"
        )

        self.lockdown_value.setObjectName(
            "settings_item_title"
        )

        self._add_readonly_row(
            security_layout,
            "Authentication",
            self.authentication_value,
        )

        self._add_readonly_row(
            security_layout,
            "Session",
            self.session_value,
        )

        self._add_readonly_row(
            security_layout,
            "Lockdown",
            self.lockdown_value,
        )

        self._add_information_row(
            security_layout,
            "Authorization",
            "Capability activation is controlled by the SecurityKernel.",
        )

        layout.addWidget(
            security
        )

        # =====================================================
        # EVOLUTION
        # =====================================================

        evolution = self._create_section(
            "Evolution",
            "KRISH never performs automatic self improvement.",
        )

        evolution_layout = (
            evolution.layout()
        )

        self._add_capability(
            evolution_layout,
            "automatic_evolution",
            "Automatic Evolution",
            "Permanently OFF. Specific evolution requires explicit owner authorization.",
        )

        self._add_information_row(
            evolution_layout,
            "Owner Authorization",
            "Required before any intentionally authorized component improvement.",
        )

        layout.addWidget(
            evolution
        )

        # =====================================================
        # APPLICATION
        # =====================================================

        application = self._create_section(
            "Application",
            "KRISH environment information.",
        )

        application_layout = (
            application.layout()
        )

        self.application_value = QLabel()
        self.python_value = QLabel()
        self.architecture_value = QLabel()

        self.application_value.setObjectName(
            "settings_item_title"
        )

        self.python_value.setObjectName(
            "settings_item_title"
        )

        self.architecture_value.setObjectName(
            "settings_item_title"
        )

        self._add_readonly_row(
            application_layout,
            "Application",
            self.application_value,
        )

        self._add_readonly_row(
            application_layout,
            "Python",
            self.python_value,
        )

        self._add_readonly_row(
            application_layout,
            "Architecture",
            self.architecture_value,
        )

        layout.addWidget(
            application
        )

        # =====================================================
        # ACTIONS
        # =====================================================

        actions = QHBoxLayout()

        refresh_button = QPushButton(
            "Refresh"
        )

        refresh_button.setObjectName(
            "primary"
        )

        refresh_button.clicked.connect(
            self.refresh
        )

        actions.addWidget(
            refresh_button
        )

        reset_button = QPushButton(
            "Reset Capabilities"
        )

        reset_button.clicked.connect(
            self._reset_capabilities
        )

        actions.addWidget(
            reset_button
        )

        actions.addStretch()

        layout.addLayout(
            actions
        )

        # =====================================================
        # MESSAGE
        # =====================================================

        self.message = QLabel()

        self.message.setWordWrap(
            True
        )

        self.message.setObjectName(
            "panel_description"
        )

        layout.addWidget(
            self.message
        )

        layout.addStretch()

        scroll.setWidget(
            content
        )

        outer.addWidget(
            scroll,
            1
        )

    # =========================================================
    # SECTIONS
    # =========================================================

    def _create_section(
        self,
        title,
        description,
    ):

        frame = QFrame()

        frame.setObjectName(
            "settings_section"
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(
            12
        )

        heading = QLabel(
            title
        )

        heading.setObjectName(
            "settings_section_title"
        )

        subheading = QLabel(
            description
        )

        subheading.setObjectName(
            "settings_section_description"
        )

        subheading.setWordWrap(
            True
        )

        layout.addWidget(
            heading
        )

        layout.addWidget(
            subheading
        )

        return frame

    # =========================================================
    # CAPABILITY ROW
    # =========================================================

    def _add_capability(
        self,
        layout,
        name,
        title,
        description,
    ):

        row = QHBoxLayout()

        labels = QVBoxLayout()

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "settings_item_title"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "settings_item_description"
        )

        description_label.setWordWrap(
            True
        )

        labels.addWidget(
            title_label
        )

        labels.addWidget(
            description_label
        )

        switch = CapabilitySwitch(
            name,
            title,
            description,
        )

        switch.changed.connect(
            lambda value, n=name:
            self._capability_changed(
                n,
                value,
            )
        )

        self.capability_switches[
            name
        ] = switch

        row.addLayout(
            labels,
            1
        )

        row.addWidget(
            switch
        )

        layout.addLayout(
            row
        )

    # =========================================================
    # INFORMATION ROW
    # =========================================================

    def _add_information_row(
        self,
        layout,
        title,
        description,
    ):

        row = QHBoxLayout()

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "settings_item_title"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "settings_item_description"
        )

        description_label.setWordWrap(
            True
        )

        row.addWidget(
            title_label
        )

        row.addStretch()

        row.addWidget(
            description_label,
            1
        )

        layout.addLayout(
            row
        )

    # =========================================================
    # READONLY ROW
    # =========================================================

    def _add_readonly_row(
        self,
        layout,
        title,
        value_widget,
    ):

        row = QHBoxLayout()

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "settings_item_title"
        )

        row.addWidget(
            title_label
        )

        row.addStretch()

        row.addWidget(
            value_widget
        )

        layout.addLayout(
            row
        )

    # =========================================================
    # THEME
    # =========================================================

    def _theme_changed(
        self,
        index,
    ):

        if self._building:
            return

        theme = self.theme_combo.itemData(
            index
        )

        if theme not in (
            THEME_DARK,
            THEME_LIGHT,
            THEME_SYSTEM,
        ):
            return

        self.settings.setValue(
            "appearance/theme",
            theme,
        )

        app = QApplication.instance()

        if app is not None:
            apply_theme(
                app,
                theme,
            )

        self._show_message(
            f"Theme changed to {theme.title()}."
        )

    def _load_theme(self):

        theme = self.settings.value(
            "appearance/theme",
            THEME_SYSTEM,
        )

        if theme not in (
            THEME_DARK,
            THEME_LIGHT,
            THEME_SYSTEM,
        ):
            theme = THEME_SYSTEM

        index = self.theme_combo.findData(
            theme
        )

        if index >= 0:

            self._building = True

            try:

                self.theme_combo.setCurrentIndex(
                    index
                )

            finally:

                self._building = False

        app = QApplication.instance()

        if app is not None:

            apply_theme(
                app,
                theme,
            )

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

    def _get_active_session_id(
        self,
        security,
    ):

        if security is None:
            return None

        getter = getattr(
            security,
            "get_active_session_id",
            None,
        )

        if not callable(getter):
            return None

        try:
            return getter()

        except Exception:
            return None

    # =========================================================
    # CAPABILITY CHANGED
    # =========================================================

    def _capability_changed(
        self,
        name,
        value,
    ):

        if self._building:
            return

        switch = (
            self.capability_switches.get(
                name
            )
        )

        if switch is None:
            return

        # =====================================================
        # AUTOMATIC EVOLUTION
        # =====================================================

        if name == "automatic_evolution":

            # Evolution is NOT a runtime capability.
            # It is permanently disabled globally.

            switch.set_value(
                False
            )

            if value:

                self._show_message(
                    "Automatic Evolution is permanently OFF. "
                    "KRISH may only perform a specifically "
                    "authorized evolution operation."
                )

            return

        # =====================================================
        # OFF
        # =====================================================

        if not value:

            success = (
                self._disable_capability(
                    name
                )
            )

            # Always force the UI to the real safe state.
            switch.set_value(
                False
            )

            if success:

                self._show_message(
                    f"{self._display_name(name)} is OFF."
                )

            else:

                self._show_message(
                    f"{self._display_name(name)} "
                    "could not be disabled."
                )

            return

        # =====================================================
        # ON
        # =====================================================

        try:

            success = (
                self._enable_capability(
                    name
                )
            )

            if success:

                switch.set_value(
                    True
                )

                self._show_message(
                    f"{self._display_name(name)} is now ON."
                )

            else:

                switch.set_value(
                    False
                )

                self._show_message(
                    f"{self._display_name(name)} "
                    "was not enabled."
                )

        except Exception as error:

            switch.set_value(
                False
            )

            self._show_message(
                f"{self._display_name(name)} "
                f"was not enabled: {error}"
            )

    # =========================================================
    # ENABLE
    # =========================================================

    def _enable_capability(
        self,
        name,
    ):

        security = self._get_security()

        if security is None:
            raise RuntimeError(
                "Security subsystem is unavailable."
            )

        # -----------------------------------------------------
        # SECURITY SESSION
        # -----------------------------------------------------

        session_id = (
            self._get_active_session_id(
                security
            )
        )

        if not session_id:

            raise PermissionError(
                "Active authenticated owner session required."
            )

        # -----------------------------------------------------
        # EVOLUTION IS NEVER A CAPABILITY
        # -----------------------------------------------------

        if name == "automatic_evolution":
            return False

        # -----------------------------------------------------
        # THE CORRECT SECURITY ENTRY POINT
        # -----------------------------------------------------
        #
        # IMPORTANT:
        #
        # Do NOT call:
        #
        #     security.enable_capability(...)
        #
        # directly from the UI.
        #
        # owner_authorize_capability() is the controlled
        # owner-side authorization path.
        # -----------------------------------------------------

        owner_authorize = getattr(
            security,
            "owner_authorize_capability",
            None,
        )

        if callable(
            owner_authorize
        ):

            result = owner_authorize(
                name,
                session_id=session_id,
            )

            return (
                True
                if result is None
                else bool(result)
            )

        # -----------------------------------------------------
        # BACKWARD COMPATIBILITY
        # -----------------------------------------------------
        #
        # Only used if an older SecurityKernel is running.
        # -----------------------------------------------------

        enable = getattr(
            security,
            "enable_capability",
            None,
        )

        if not callable(
            enable
        ):

            raise RuntimeError(
                "SecurityKernel does not expose "
                "a capability authorization interface."
            )

        try:

            result = enable(
                name,
                session_id=session_id,
            )

        except TypeError:

            result = enable(
                capability=name,
                session_id=session_id,
            )

        return (
            True
            if result is None
            else bool(result)
        )

    # =========================================================
    # DISABLE
    # =========================================================

    def _disable_capability(
        self,
        name,
    ):

        # -----------------------------------------------------
        # Automatic evolution is not a capability.
        # -----------------------------------------------------

        if name == "automatic_evolution":
            return True

        security = self._get_security()

        if security is None:
            return False

        disable = getattr(
            security,
            "disable_capability",
            None,
        )

        if not callable(
            disable
        ):
            return False

        try:

            result = disable(
                name
            )

            return (
                True
                if result is None
                else bool(result)
            )

        except Exception:

            return False

    # =========================================================
    # RESET
    # =========================================================

    def _reset_capabilities(self):

        security = self._get_security()

        if security is None:

            self._show_message(
                "Security subsystem is unavailable."
            )

            return

        reset = getattr(
            security,
            "reset_capabilities",
            None,
        )

        if callable(
            reset
        ):

            try:

                reset()

                # Evolution is always OFF.
                for switch in (
                    self.capability_switches.values()
                ):
                    switch.set_value(
                        False
                    )

                self.refresh()

                self._show_message(
                    "All runtime capabilities reset to OFF."
                )

                return

            except Exception as error:

                self._show_message(
                    f"Capability reset failed: {error}"
                )

                return

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        for name in (
            self.capability_switches
        ):

            self._disable_capability(
                name
            )

        self.refresh()

        self._show_message(
            "All runtime capabilities reset to OFF."
        )

    # =========================================================
    # READ CAPABILITIES
    # =========================================================

    def _read_capabilities(self):

        security = self._get_security()

        if security is None:
            return {}

        getter = getattr(
            security,
            "capabilities",
            None,
        )

        if callable(
            getter
        ):

            try:

                result = getter()

                if isinstance(
                    result,
                    dict,
                ):
                    return dict(
                        result
                    )

            except Exception:
                pass

        getter = getattr(
            security,
            "capability_state",
            None,
        )

        if callable(
            getter
        ):

            try:

                result = getter()

                if isinstance(
                    result,
                    dict,
                ):
                    return dict(
                        result
                    )

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
            return dict(
                value
            )

        return {}

    # =========================================================
    # PROVIDER
    # =========================================================

    def _find_provider(self):

        brain = getattr(
            self.krish,
            "brain",
            None,
        )

        if brain is None:
            return None

        provider = getattr(
            brain,
            "provider",
            None,
        )

        if provider is not None:
            return provider

        return getattr(
            brain,
            "_provider",
            None,
        )

    def _provider_name(self):

        provider = (
            self._find_provider()
        )

        if provider is None:
            return "Unknown"

        for attribute in (
            "name",
            "provider_name",
            "provider_type",
        ):

            value = getattr(
                provider,
                attribute,
                None,
            )

            if value:
                return str(
                    value
                )

        return type(
            provider
        ).__name__

    def _model_name(self):

        provider = (
            self._find_provider()
        )

        if provider is None:
            return "Unknown"

        for attribute in (
            "model",
            "model_name",
        ):

            value = getattr(
                provider,
                attribute,
                None,
            )

            if value:
                return str(
                    value
                )

        config = getattr(
            self.krish,
            "config",
            None,
        )

        if config is not None:

            for attribute in (
                "model",
                "ai_model",
            ):

                value = getattr(
                    config,
                    attribute,
                    None,
                )

                if value:
                    return str(
                        value
                    )

        return "Unknown"

    # =========================================================
    # SECURITY INFORMATION
    # =========================================================

    def _security_status(self):

        security = (
            self._get_security()
        )

        if security is None:

            return (
                "Unavailable",
                "Unavailable",
                "Unavailable",
            )

        authenticated = False

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

        session_id = (
            self._get_active_session_id(
                security
            )
        )

        lockdown_active = False

        lockdown = getattr(
            security,
            "lockdown",
            None,
        )

        if lockdown is not None:

            lockdown_active = bool(
                getattr(
                    lockdown,
                    "active",
                    getattr(
                        lockdown,
                        "engaged",
                        False,
                    ),
                )
            )

        return (
            "Authenticated"
            if authenticated
            else "Not authenticated",

            "Active"
            if session_id
            else "No active session",

            "LOCKDOWN"
            if lockdown_active
            else "Normal",
        )

    # =========================================================
    # DISPLAY NAME
    # =========================================================

    @staticmethod
    def _display_name(
        name,
    ):

        return name.replace(
            "_",
            " ",
        ).title()

    # =========================================================
    # MESSAGE
    # =========================================================

    def _show_message(
        self,
        message,
    ):

        self.message.setText(
            str(message)
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        self._load_theme()

        capabilities = (
            self._read_capabilities()
        )

        self._building = True

        try:

            for (
                name,
                switch,
            ) in self.capability_switches.items():

                # -------------------------------------------------
                # AUTOMATIC EVOLUTION
                # -------------------------------------------------

                if name == "automatic_evolution":

                    switch.set_value(
                        False
                    )

                    continue

                # -------------------------------------------------
                # NORMAL CAPABILITY
                # -------------------------------------------------

                value = bool(
                    capabilities.get(
                        name,
                        False,
                    )
                )

                switch.set_value(
                    value
                )

        finally:

            self._building = False

        # =========================================================
        # APPLICATION
        # =========================================================

        self.application_value.setText(
            type(
                self.krish
            ).__name__
        )

        self.python_value.setText(
            "3.12"
        )

        self.architecture_value.setText(
            "Local-first"
        )

        # =========================================================
        # AI
        # =========================================================

        self.provider_value.setText(
            self._provider_name()
        )

        self.model_value.setText(
            self._model_name()
        )

        # =========================================================
        # SECURITY
        # =========================================================

        (
            authentication,
            session,
            lockdown,
        ) = self._security_status()

        self.authentication_value.setText(
            authentication
        )

        self.session_value.setText(
            session
        )

        self.lockdown_value.setText(
            lockdown
        )