# ui/application.py

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog

from main import Krish
from ui.auth_window import AuthenticationWindow
from ui.main_window import KrishMainWindow
from ui.theme import KRISH_STYLE


class KrishApplication:
    """
    Top-level KRISH desktop application.

    Responsibilities:
    - Create the Qt application.
    - Configure global application metadata.
    - Apply the initial UI theme.
    - Initialize KRISH backend services.
    - Authenticate the owner before opening the main UI.
    - Start the Qt event loop.
    - Perform safe shutdown.
    """

    def __init__(self):
        self.application = QApplication(sys.argv)

        self.application.setApplicationName("KRISH")
        self.application.setApplicationDisplayName(
            "KRISH Personal AI"
        )
        self.application.setOrganizationName("KRISH")

        # Use high quality rendering where supported.
        self.application.setAttribute(
            Qt.ApplicationAttribute.AA_UseHighDpiPixmaps,
            True,
        )

        # Current default theme.
        #
        # The full Dark / Light / System theme selector
        # will be centralized in ui.theme rather than
        # duplicated throughout the application.
        self.application.setStyleSheet(KRISH_STYLE)

        self.krish = None
        self.window = None
        self.auth_window = None

        self._initialized = False
        self._shutdown_complete = False

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def initialize(self):
        """
        Initialize the KRISH backend.

        Returns:
            bool: True when initialization succeeds.
        """
        if self._initialized:
            return True

        self.krish = Krish()
        self.krish.initialize()

        self._initialized = True

        return True

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate_owner(self):
        """
        Display the owner authentication window.

        Returns:
            bool: True only when authentication succeeds.
        """
        if self.krish is None:
            raise RuntimeError(
                "KRISH backend has not been initialized."
            )

        # Determine whether this is the first KRISH startup.
        first_time = not (
            self.krish.security.has_configured_secret()
        )

        self.auth_window = AuthenticationWindow(
            self.krish,
            first_time=first_time,
        )

        result = self.auth_window.exec()

        # Always release the authentication window reference
        # after the modal operation completes.
        auth_window = self.auth_window
        self.auth_window = None

        if auth_window is not None:
            auth_window.deleteLater()

        if result != QDialog.DialogCode.Accepted:
            return False

        # AuthenticationWindow is responsible for authenticating
        # the owner through the KRISH security layer.
        #
        # Do not trust the dialog result alone. Verify that KRISH
        # actually has an authenticated security state and an
        # active owner session.
        if not self.krish.security.authentication.authenticated:
            return False

        session_id = self.krish.security.get_active_session_id()

        if not session_id:
            return False

        if not self.krish.security.session.validate(
            session_id
        ):
            return False

        return True

    # ------------------------------------------------------------------
    # Main window
    # ------------------------------------------------------------------

    def create_main_window(self):
        """
        Create the authenticated KRISH main window.
        """
        if self.krish is None:
            raise RuntimeError(
                "KRISH backend has not been initialized."
            )

        if not self.krish.security.authentication.authenticated:
            raise PermissionError(
                "Owner authentication required."
            )

        session_id = self.krish.security.get_active_session_id()

        if not session_id:
            raise PermissionError(
                "Active owner session required."
            )

        if not self.krish.security.session.validate(
            session_id
        ):
            raise PermissionError(
                "Owner session is invalid or expired."
            )

        self.window = KrishMainWindow(self.krish)

        return self.window

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    def run(self):
        """
        Start the KRISH desktop application.
        """
        try:
            self.initialize()

            # Owner authentication must succeed before the
            # main KRISH interface becomes available.
            if not self.authenticate_owner():
                self.shutdown()
                return 0

            self.create_main_window()

            self.window.show()

            # Start the Qt event loop.
            exit_code = self.application.exec()

            return exit_code

        except KeyboardInterrupt:
            return 0

        except Exception as error:
            # Do not leave the backend running after a startup
            # or runtime failure.
            print(
                f"KRISH application error: {error}",
                file=sys.stderr,
            )

            return 1

        finally:
            self.shutdown()

    # ------------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------------

    def shutdown(self):
        """
        Safely shut down KRISH exactly once.
        """
        if self._shutdown_complete:
            return

        self._shutdown_complete = True

        try:
            if self.window is not None:
                self.window.close()
                self.window.deleteLater()
                self.window = None
        except Exception:
            pass

        try:
            if self.auth_window is not None:
                self.auth_window.close()
                self.auth_window.deleteLater()
                self.auth_window = None
        except Exception:
            pass

        try:
            if self.krish is not None:
                self.krish.shutdown()
        except Exception as error:
            print(
                f"KRISH shutdown warning: {error}",
                file=sys.stderr,
            )

        self.krish = None


if __name__ == "__main__":
    raise SystemExit(
        KrishApplication().run()
    )