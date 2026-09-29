from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
)

from ui.components.chat_view import ChatView
from ui.components.input_bar import InputBar
from ui.components.status_bar import KrishStatusBar
from ui.controllers.chat_controller import ChatController

from ui.panels.dashboard import DashboardPanel
from ui.panels.memory import MemoryPanel
from ui.panels.security import SecurityPanel
from ui.panels.tools import ToolsPanel
from ui.panels.agent import AgentPanel
from ui.panels.evolution import EvolutionPanel
from ui.panels.settings import SettingsPanel


class KrishMainWindow(QMainWindow):

    def __init__(self, krish):
        super().__init__()

        self.krish = krish

        self.setWindowTitle("KRISH Personal AI")
        self.setMinimumSize(1180, 720)
        self.resize(1360, 840)

        self.chat_controller = ChatController(krish)

        self.chat_controller.response_chunk.connect(
            self._handle_chunk
        )
        self.chat_controller.response_ready.connect(
            self._handle_response
        )
        self.chat_controller.error_occurred.connect(
            self._handle_error
        )
        self.chat_controller.processing_started.connect(
            self._processing_started
        )
        self.chat_controller.processing_finished.connect(
            self._processing_finished
        )

        self._build_ui()

        self.refresh_conversations()
        self._show_chat_page()
        self._load_current_conversation()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):

        central = QWidget()
        central.setObjectName("main_container")

        main = QHBoxLayout(central)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        self.sidebar = self._build_sidebar()

        right = QWidget()

        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        right_layout.addWidget(self._build_topbar())

        self.pages = QStackedWidget()

        self.chat_page = self._build_chat_page()

        self.dashboard_page = DashboardPanel(self.krish)
        self.memory_page = MemoryPanel(self.krish)
        self.security_page = SecurityPanel(self.krish)
        self.tools_page = ToolsPanel(self.krish)
        self.agent_page = AgentPanel(self.krish)
        self.evolution_page = EvolutionPanel(self.krish)
        self.settings_page = SettingsPanel(self.krish)

        pages = [
            self.chat_page,
            self.dashboard_page,
            self.memory_page,
            self.security_page,
            self.tools_page,
            self.agent_page,
            self.evolution_page,
            self.settings_page,
        ]

        for page in pages:
            self.pages.addWidget(page)

        self.statusbar = KrishStatusBar()

        right_layout.addWidget(self.pages, 1)
        right_layout.addWidget(self.statusbar)

        main.addWidget(self.sidebar)
        main.addWidget(right, 1)

        self.setCentralWidget(central)

    # =========================================================
    # SIDEBAR
    # =========================================================

    def _build_sidebar(self):

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(270)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 24, 18, 18)
        layout.setSpacing(7)

        logo = QLabel("KRISH")
        logo.setObjectName("logo")

        subtitle = QLabel("PERSONAL AI SYSTEM")
        subtitle.setObjectName("logo_subtitle")

        layout.addWidget(logo)
        layout.addWidget(subtitle)
        layout.addSpacing(18)

        self.new_chat_button = QPushButton("+  New Chat")
        self.new_chat_button.setObjectName("primary")
        self.new_chat_button.clicked.connect(
            self._new_chat
        )

        layout.addWidget(self.new_chat_button)

        self.chat_list = QListWidget()
        self.chat_list.setObjectName("conversation_list")
        self.chat_list.itemClicked.connect(
            self._conversation_selected
        )

        layout.addWidget(self.chat_list, 1)

        self.nav_buttons = []

        navigation = [
            ("Chat", 0),
            ("Dashboard", 1),
            ("Memory", 2),
            ("Security", 3),
            ("Tools", 4),
            ("Agent", 5),
            ("Evolution", 6),
            ("Settings", 7),
        ]

        for text, index in navigation:

            button = self._create_nav_button(
                text,
                index,
            )

            self.nav_buttons.append(button)

            layout.addWidget(button)

        layout.addSpacing(12)

        system_label = QLabel("SYSTEM")
        system_label.setObjectName("logo_subtitle")

        layout.addWidget(system_label)

        self.runtime_label = QLabel("● READY")
        self.runtime_label.setObjectName("status_active")

        layout.addWidget(self.runtime_label)

        return sidebar

    def _create_nav_button(self, text, index):

        button = QPushButton(text)

        button.setCheckable(True)
        button.setAutoExclusive(True)
        button.setObjectName("nav_button")

        button.clicked.connect(
            lambda checked=False, i=index:
            self._switch_page(i)
        )

        return button

    # =========================================================
    # TOP BAR
    # =========================================================

    def _build_topbar(self):

        topbar = QFrame()
        topbar.setObjectName("topbar")

        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(
            24,
            15,
            24,
            15,
        )

        title_container = QWidget()

        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        title_layout.setSpacing(2)

        self.page_title = QLabel("Chat")
        self.page_title.setObjectName("page_title")

        self.page_subtitle = QLabel(
            "Your conversations stay available locally"
        )
        self.page_subtitle.setObjectName("page_subtitle")

        title_layout.addWidget(self.page_title)
        title_layout.addWidget(self.page_subtitle)

        layout.addWidget(title_container)
        layout.addStretch()

        self.top_status = QLabel("KRISH • LOCAL")
        self.top_status.setObjectName("status_active")

        layout.addWidget(self.top_status)

        return topbar

    # =========================================================
    # CHAT
    # =========================================================

    def _build_chat_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(0)

        self.chat = ChatView()
        self.input_bar = InputBar()

        layout.addWidget(self.chat, 1)
        layout.addWidget(self.input_bar)

        self.input_bar.message_sent.connect(
            self._send_message
        )

        self.input_bar.voice_requested.connect(
            self._voice_requested
        )

        self.input_bar.stop_requested.connect(
            self._stop_response
        )

        return page

    # =========================================================
    # NAVIGATION
    # =========================================================

    def _switch_page(self, index):

        if index < 0 or index >= self.pages.count():
            return

        self.pages.setCurrentIndex(index)

        for button in self.nav_buttons:
            button.setChecked(False)

        if index < len(self.nav_buttons):
            self.nav_buttons[index].setChecked(True)

        titles = {
            0: (
                "Chat",
                "Your conversations stay available locally",
            ),
            1: (
                "Dashboard",
                "KRISH system overview and runtime information",
            ),
            2: (
                "Memory",
                "Persistent memory and conversation retrieval",
            ),
            3: (
                "Security",
                "Owner authentication, permissions and security controls",
            ),
            4: (
                "Tools",
                "Available KRISH tools and permission states",
            ),
            5: (
                "Agent",
                "Planning, execution, verification and recovery",
            ),
            6: (
                "Evolution",
                "Owner controlled improvement and verification",
            ),
            7: (
                "Settings",
                "KRISH application configuration",
            ),
        }

        title, subtitle = titles[index]

        self.page_title.setText(title)
        self.page_subtitle.setText(subtitle)

        self._refresh_current_panel(index)

    def _refresh_current_panel(self, index):

        page = self.pages.widget(index)

        refresh = getattr(
            page,
            "refresh",
            None,
        )

        if callable(refresh):
            try:
                refresh()
            except Exception:
                pass

    def _show_chat_page(self):
        self._switch_page(0)

    # =========================================================
    # CONVERSATIONS
    # =========================================================

    def refresh_conversations(self, select_id=None):

        try:
            conversations = self.krish.list_conversations()
        except Exception:
            return

        self.chat_list.blockSignals(True)

        try:
            self.chat_list.clear()

            target_id = (
                select_id
                or getattr(
                    self.krish,
                    "conversation_id",
                    None,
                )
            )

            target_row = -1

            for row, conversation in enumerate(
                conversations
            ):

                conversation_id = conversation.get(
                    "conversation_id"
                )

                if not conversation_id:
                    continue

                title = conversation.get(
                    "title",
                    "New Conversation",
                )

                item = QListWidgetItem(title)

                item.setData(
                    Qt.ItemDataRole.UserRole,
                    conversation_id,
                )

                self.chat_list.addItem(item)

                if conversation_id == target_id:
                    target_row = (
                        self.chat_list.count() - 1
                    )

            if target_row >= 0:
                self.chat_list.setCurrentRow(
                    target_row
                )

        finally:
            self.chat_list.blockSignals(False)

    def _load_current_conversation(self):

        try:
            messages = (
                self.krish
                .memory
                .conversation
                .recent(1000)
            )

            self.chat.load_messages(messages)

        except Exception:
            self.chat.clear()

    def _conversation_selected(self, item):

        if self.chat_controller.busy:
            return

        conversation_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        current_id = getattr(
            self.krish,
            "conversation_id",
            None,
        )

        if conversation_id == current_id:
            return

        try:
            self.krish.load_conversation(
                conversation_id
            )

            messages = (
                self.krish
                .memory
                .conversation
                .recent(1000)
            )

            self.chat.load_messages(messages)

            self._show_chat_page()

        except Exception as error:

            self.chat.add_message(
                "KRISH",
                f"Unable to load conversation: {error}",
            )

    def _new_chat(self):

        if self.chat_controller.busy:
            return

        try:
            conversation_id = (
                self.krish.new_conversation()
            )

            self.chat.clear()

            self.refresh_conversations(
                conversation_id
            )

            self._show_chat_page()

            self.input_bar.input.setFocus()

        except Exception as error:

            self.chat.add_message(
                "KRISH",
                f"Unable to create conversation: {error}",
            )

    # =========================================================
    # MESSAGE PROCESSING
    # =========================================================

    def _send_message(self, message):

        message = message.strip()

        if not message:
            return

        if self.chat_controller.busy:
            return

        self.chat.add_message(
            "YOU",
            message,
        )

        self.chat.begin_stream()

        self._set_processing_state(True)

        self.chat_controller.send_message(
            message
        )

    def _handle_chunk(self, chunk):

        if not chunk:
            return

        self.chat.append_stream(chunk)

    def _handle_response(self, response):

        self.chat.finish_stream()

        self.refresh_conversations()

    def _handle_error(self, error):

        self.chat.finish_stream()

        if error:
            self.chat.add_message(
                "KRISH",
                f"Error: {error}",
            )

    def _stop_response(self):

        if not self.chat_controller.busy:
            return

        self.chat_controller.stop()

        self.chat.finish_stream()

        self._set_processing_state(False)

        self._set_runtime_ready()

    # =========================================================
    # PROCESSING STATE
    # =========================================================

    def _processing_started(self):

        self.runtime_label.setText(
            "● PROCESSING"
        )

        self.runtime_label.setObjectName(
            "status_warning"
        )

        self._repolish(
            self.runtime_label
        )

    def _processing_finished(self):

        self._set_runtime_ready()

        self._set_processing_state(False)

    def _set_runtime_ready(self):

        self.runtime_label.setText(
            "● READY"
        )

        self.runtime_label.setObjectName(
            "status_active"
        )

        self._repolish(
            self.runtime_label
        )

    @staticmethod
    def _repolish(widget):

        style = widget.style()

        style.unpolish(widget)
        style.polish(widget)
        widget.update()

    def _set_processing_state(self, processing):

        self.input_bar.input.setEnabled(
            not processing
        )

        self.input_bar.send_button.setVisible(
            not processing
        )

        self.input_bar.stop_button.setVisible(
            processing
        )

        self.input_bar.voice_button.setEnabled(
            not processing
        )

        self.new_chat_button.setEnabled(
            not processing
        )

        self.chat_list.setEnabled(
            not processing
        )

        if not processing:
            self.input_bar.input.setFocus()

    def _voice_requested(self):

        self.chat.add_message(
            "KRISH",
            "Voice input is not connected yet.",
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def closeEvent(self, event):

        try:
            self.chat_controller.stop()
        except Exception:
            pass

        event.accept()