from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class AuthenticationWindow(QDialog):
    """
    KRISH owner authentication and initial credential setup.

    This window is responsible only for:
    - Creating the owner's initial secret.
    - Authenticating the owner.
    - Creating the authenticated owner session.
    - Starting the KRISH runtime.
    - Warming up the AI model.

    It does NOT enable Internet, File, System, Voice,
    or other elevated capabilities.
    """

    authenticated = Signal()
    authentication_failed = Signal(str)

    def __init__(self, krish, first_time=False):
        super().__init__()

        self.krish = krish
        self.first_time = bool(first_time)

        self.setWindowTitle("KRISH Authentication")

        self.setFixedSize(
            440,
            360,
        )

        self._authenticating = False

        self._build_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            40,
            35,
            40,
            35,
        )

        layout.setSpacing(12)

        title = QLabel("KRISH")

        title.setObjectName(
            "auth_title"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "OWNER AUTHENTICATION"
            if not self.first_time
            else "CREATE OWNER CREDENTIAL"
        )

        subtitle.setObjectName(
            "auth_subtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        if self.first_time:
            self._build_creation_fields(layout)
        else:
            self._build_authentication_field(layout)

        self.status_label = QLabel("")

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label.setWordWrap(True)

        layout.addWidget(
            self.status_label
        )

        layout.addStretch()

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Exit")

        self.authenticate_button = QPushButton(
            "Create"
            if self.first_time
            else "Authenticate"
        )

        self.authenticate_button.clicked.connect(
            self.authenticate
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        button_layout.addWidget(
            self.cancel_button
        )

        button_layout.addWidget(
            self.authenticate_button
        )

        layout.addLayout(button_layout)

    def _build_creation_fields(self, layout):
        secret_label = QLabel(
            "Create Owner Secret"
        )

        self.secret_input = QLineEdit()

        self.secret_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.secret_input.setPlaceholderText(
            "Enter a secure secret"
        )

        self.secret_input.returnPressed.connect(
            self.authenticate
        )

        confirm_label = QLabel(
            "Confirm Owner Secret"
        )

        self.confirm_input = QLineEdit()

        self.confirm_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.confirm_input.setPlaceholderText(
            "Confirm your secret"
        )

        self.confirm_input.returnPressed.connect(
            self.authenticate
        )

        layout.addWidget(
            secret_label
        )

        layout.addWidget(
            self.secret_input
        )

        layout.addWidget(
            confirm_label
        )

        layout.addWidget(
            self.confirm_input
        )

    def _build_authentication_field(self, layout):
        secret_label = QLabel(
            "Owner Secret"
        )

        self.secret_input = QLineEdit()

        self.secret_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.secret_input.setPlaceholderText(
            "Enter your owner secret"
        )

        self.secret_input.returnPressed.connect(
            self.authenticate
        )

        layout.addWidget(
            secret_label
        )

        layout.addWidget(
            self.secret_input
        )

        self.secret_input.setFocus()

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self):
        """
        Create or authenticate the owner and establish
        an authenticated session.
        """
        if self._authenticating:
            return

        secret = self.secret_input.text()

        if not secret:
            self._show_error(
                "Secret cannot be empty."
            )
            return

        if self.first_time:
            if not self._create_owner_secret(secret):
                return

        else:
            if not self._authenticate_existing_owner(secret):
                return

        if not self._create_authenticated_session():
            return

        self._authentication_success()

    # ------------------------------------------------------------------
    # First-time setup
    # ------------------------------------------------------------------

    def _create_owner_secret(self, secret):
        confirmation = self.confirm_input.text()

        if not confirmation:
            self._show_error(
                "Please confirm your secret."
            )
            return False

        if secret != confirmation:
            self._show_error(
                "Secrets do not match."
            )
            return False

        try:
            self.krish.security.configure_secret(
                secret
            )

            # Configuring a secret intentionally resets
            # authentication state. Explicitly authenticate
            # the newly configured secret so that first-time
            # setup produces the same authenticated state as
            # subsequent startups.
            authenticated = (
                self.krish.security.authenticate(
                    secret
                )
            )

            if not authenticated:
                self._show_error(
                    "Owner credential creation failed."
                )
                return False

        except Exception as error:
            self._show_error(
                str(error)
            )
            return False

        return True

    # ------------------------------------------------------------------
    # Existing owner authentication
    # ------------------------------------------------------------------

    def _authenticate_existing_owner(self, secret):
        try:
            authenticated = (
                self.krish.security.authenticate(
                    secret
                )
            )

        except Exception as error:
            self._show_error(
                str(error)
            )
            return False

        if not authenticated:
            self.authentication_failed.emit(
                "Authentication failed."
            )

            self._show_error(
                "Authentication failed."
            )

            return False

        return True

    # ------------------------------------------------------------------
    # Session initialization
    # ------------------------------------------------------------------

    def _create_authenticated_session(self):
        """
        Establish the authenticated owner session and
        initialize the runtime.

        No elevated capabilities are enabled here.
        """
        self._set_busy(True)

        try:
            session = (
                self.krish.security.create_session()
            )

            if session is None:
                self._show_error(
                    "Unable to create owner session."
                )
                return False

            self.krish.session = session

            # Only baseline, non-elevated permissions.
            #
            # This must NOT enable:
            # - Internet
            # - Web Search
            # - External Data
            # - File Access
            # - System Access
            # - Application Launch
            # - Python / Terminal
            # - Voice
            #
            # Those capabilities remain OFF until explicitly
            # enabled through the security layer.
            self.krish.grant_basic_permissions()

            # Start the runtime only after successful owner
            # authentication and session creation.
            self.krish.runtime.start()

            # Warm the local model so the first response is
            # faster.
            self.krish.warmup_model()

        except Exception as error:
            self._show_error(
                str(error)
            )
            return False

        finally:
            self._set_busy(False)

        return True

    # ------------------------------------------------------------------
    # Success
    # ------------------------------------------------------------------

    def _authentication_success(self):
        self.status_label.setText(
            "Authentication successful."
        )

        self.authenticated.emit()

        self.accept()

    # ------------------------------------------------------------------
    # UI state
    # ------------------------------------------------------------------

    def _set_busy(self, busy):
        self._authenticating = busy

        self.authenticate_button.setEnabled(
            not busy
        )

        self.cancel_button.setEnabled(
            not busy
        )

        self.secret_input.setEnabled(
            not busy
        )

        if self.first_time:
            self.confirm_input.setEnabled(
                not busy
            )

    def _show_error(self, message):
        self.status_label.setText(
            str(message)
        )

        self.secret_input.clear()

        if self.first_time:
            self.confirm_input.clear()

        self.secret_input.setFocus()