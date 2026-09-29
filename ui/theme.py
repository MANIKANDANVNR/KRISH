from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication


# =============================================================
# KRISH THEME SYSTEM
# =============================================================

THEME_DARK = "dark"
THEME_LIGHT = "light"
THEME_SYSTEM = "system"

THEMES = (
    THEME_DARK,
    THEME_LIGHT,
    THEME_SYSTEM,
)


# =============================================================
# DARK THEME
# =============================================================

KRISH_STYLE = """
QApplication {
    background-color: #0b0f14;
    color: #dce3ea;
}

QMainWindow {
    background-color: #0b0f14;
    color: #dce3ea;
}

QWidget {
    font-family: "Segoe UI";
    font-size: 13px;
    color: #dce3ea;
}

QLabel {
    color: #aeb8c3;
}


/* MAIN WINDOW */

QFrame#sidebar {
    background-color: #0e131a;
    border-right: 1px solid #202832;
}

QFrame#topbar {
    background-color: #0b0f14;
    border-bottom: 1px solid #202832;
}

QFrame#statusbar {
    background-color: #0e131a;
    border-top: 1px solid #202832;
}


/* BRANDING */

QLabel#logo {
    color: #ffffff;
    font-size: 24px;
    font-weight: 700;
}

QLabel#logo_subtitle {
    color: #66717e;
    font-size: 10px;
}

QLabel#page_title {
    color: #ffffff;
    font-size: 20px;
    font-weight: 600;
}

QLabel#page_subtitle {
    color: #707c89;
    font-size: 11px;
}


/* STATUS */

QLabel#system_status {
    color: #7f8b98;
    font-size: 11px;
}

QLabel#system_status_active,
QLabel#status_active {
    color: #8fa99a;
    font-size: 11px;
}

QLabel#status_inactive {
    color: #707b87;
    font-size: 11px;
}

QLabel#status_warning {
    color: #b69f72;
    font-size: 11px;
}

QLabel#status_error {
    color: #b87575;
    font-size: 11px;
}


/* NAVIGATION */

QPushButton#nav_button {
    background-color: transparent;
    color: #8995a2;
    border: none;
    border-radius: 7px;
    padding: 11px 14px;
    text-align: left;
    font-size: 13px;
}

QPushButton#nav_button:hover {
    background-color: #151b23;
    color: #dce3ea;
}

QPushButton#nav_button:checked {
    background-color: #1a222c;
    color: #ffffff;
    border-left: 2px solid #8798a9;
}

QPushButton#nav_button:pressed {
    background-color: #202933;
}


/* BUTTONS */

QPushButton {
    background-color: #151b23;
    color: #dce3ea;
    border: 1px solid #303945;
    border-radius: 8px;
    padding: 9px 15px;
}

QPushButton:hover {
    background-color: #202833;
    border-color: #3b4653;
}

QPushButton:pressed {
    background-color: #10151b;
}

QPushButton:disabled {
    background-color: #10151b;
    color: #4f5964;
    border-color: #242b33;
}

QPushButton#primary,
QPushButton#send {
    background-color: #202a35;
    color: #ffffff;
    border: 1px solid #465362;
    font-weight: 600;
}

QPushButton#primary:hover,
QPushButton#send:hover {
    background-color: #2a3643;
}

QPushButton#primary:pressed,
QPushButton#send:pressed {
    background-color: #182029;
}


/* STOP */

QPushButton#stop {
    background-color: #2a2020;
    color: #e4caca;
    border: 1px solid #604343;
    border-radius: 8px;
    padding: 9px 18px;
    font-weight: 600;
}

QPushButton#stop:hover {
    background-color: #352626;
    border-color: #785252;
}

QPushButton#stop:pressed {
    background-color: #211818;
}


/* VOICE */

QPushButton#voice {
    background-color: #151b23;
    color: #b9c4ce;
    border: 1px solid #303945;
    border-radius: 8px;
    padding: 9px 13px;
    font-size: 15px;
}

QPushButton#voice:hover {
    background-color: #202833;
    color: #ffffff;
}


/* CHAT */

QFrame#chat_area,
QScrollArea,
QScrollArea > QWidget > QWidget {
    background-color: #0b0f14;
    border: none;
}


/* MESSAGE */

QFrame#message,
QFrame#message_krish {
    background-color: #10161e;
    border: 1px solid #222d38;
    border-radius: 10px;
}

QFrame#message_user {
    background-color: #151d27;
    border: 1px solid #283440;
    border-radius: 10px;
}

QLabel#message_sender,
QLabel#message_sender_krish,
QLabel#message_sender_user {
    color: #8d99a6;
    font-size: 10px;
    font-weight: 700;
}

QLabel#message_text,
QLabel#message_text_krish,
QLabel#message_text_user {
    color: #dce3ea;
    font-size: 13px;
}


/* INPUT */

QFrame#input_bar {
    background-color: #0b0f14;
    border-top: 1px solid #202832;
}

QLineEdit,
QLineEdit#input {
    background-color: #151b23;
    color: #ffffff;
    border: 1px solid #303945;
    border-radius: 9px;
    padding: 11px 14px;
    selection-background-color: #34414f;
}

QLineEdit:focus {
    border: 1px solid #596878;
}

QLineEdit:disabled {
    background-color: #10151b;
    color: #59636e;
}


/* TEXT EDIT */

QTextEdit {
    background-color: #111720;
    color: #dce3ea;
    border: 1px solid #303945;
    border-radius: 8px;
    padding: 8px;
}

QTextEdit:focus {
    border: 1px solid #667789;
}


/* COMBO */

QComboBox {
    background-color: #151b23;
    color: #dce3ea;
    border: 1px solid #303945;
    border-radius: 8px;
    padding: 8px 10px;
}

QComboBox:hover {
    border-color: #46515e;
}

QComboBox QAbstractItemView {
    background-color: #151b23;
    color: #dce3ea;
    border: 1px solid #303945;
    selection-background-color: #202a35;
}


/* CHECKBOX */

QCheckBox {
    color: #b8c2cc;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    background-color: #151b23;
    border: 1px solid #3a4551;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #596878;
    border: 1px solid #6e7f90;
    border-radius: 4px;
}


/* GROUP BOX */

QGroupBox {
    background-color: #10161e;
    color: #dce3ea;
    border: 1px solid #242e39;
    border-radius: 9px;
    margin-top: 12px;
    padding: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #9ca8b4;
}


/* DIALOG */

QDialog {
    background-color: #0b0f14;
    color: #dce3ea;
}

QDialog QLineEdit {
    background-color: #151b23;
    color: #ffffff;
    border: 1px solid #303945;
    border-radius: 8px;
    padding: 10px 12px;
}


/* CARDS */

QFrame#card,
QFrame#settings_section {
    background-color: #10161e;
    border: 1px solid #242e39;
    border-radius: 10px;
}

QLabel#card_title {
    color: #7f8b98;
    font-size: 11px;
    font-weight: 600;
}

QLabel#card_value {
    color: #ffffff;
    font-size: 22px;
    font-weight: 700;
}


/* PANELS */

QLabel#panel_title {
    color: #ffffff;
    font-size: 18px;
    font-weight: 600;
}

QLabel#panel_description {
    color: #7f8b98;
    font-size: 12px;
}


/* SETTINGS */

QLabel#settings_section_title {
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
}

QLabel#settings_section_description {
    color: #707c89;
    font-size: 11px;
}

QLabel#settings_item_title {
    color: #dce3ea;
    font-size: 13px;
    font-weight: 600;
}

QLabel#settings_item_description {
    color: #707c89;
    font-size: 11px;
}

QLabel#capability_on {
    color: #8fa99a;
    font-size: 11px;
    font-weight: 600;
}

QLabel#capability_off {
    color: #707b87;
    font-size: 11px;
}


/* SWITCH */

QPushButton#switch_off,
QPushButton#switch_on {
    min-width: 70px;
    max-width: 70px;
    min-height: 30px;
    max-height: 30px;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 11px;
    font-weight: 600;
}

QPushButton#switch_off {
    background-color: #151b23;
    color: #7f8b98;
    border: 1px solid #303945;
}

QPushButton#switch_off:hover {
    background-color: #202833;
}

QPushButton#switch_on {
    background-color: #26352f;
    color: #b8d0c1;
    border: 1px solid #50675b;
}

QPushButton#switch_on:hover {
    background-color: #30433a;
}


/* TABLE */

QTableWidget,
QTableView {
    background-color: #10161e;
    alternate-background-color: #111922;
    color: #dce3ea;
    border: 1px solid #242e39;
    gridline-color: #202a34;
    selection-background-color: #202a35;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #151b23;
    color: #8f9ba7;
    border: none;
    padding: 8px;
    font-weight: 600;
}


/* TOOLTIP */

QToolTip {
    background-color: #151b23;
    color: #dce3ea;
    border: 1px solid #303945;
    padding: 6px;
}


/* SCROLLBARS */

QScrollBar:vertical {
    background-color: #0b0f14;
    width: 9px;
}

QScrollBar::handle:vertical {
    background-color: #303945;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #46515e;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background-color: #0b0f14;
    height: 9px;
}

QScrollBar::handle:horizontal {
    background-color: #303945;
    border-radius: 4px;
    min-width: 30px;
}


/* EVOLUTION / SECURITY */

QLabel#evolution_warning,
QLabel#approval_warning {
    color: #b69f72;
    font-weight: 600;
}


/* FOCUS */

QPushButton:focus,
QLineEdit:focus,
QTextEdit:focus,
QComboBox:focus {
    outline: none;
}
"""


# =============================================================
# LIGHT THEME
# =============================================================

KRISH_LIGHT_STYLE = """
QApplication {
    background-color: #f5f7fa;
    color: #20252b;
}

QMainWindow {
    background-color: #f5f7fa;
    color: #20252b;
}

QWidget {
    font-family: "Segoe UI";
    font-size: 13px;
    color: #20252b;
}

QLabel {
    color: #56606b;
}


/* MAIN WINDOW */

QFrame#sidebar {
    background-color: #edf0f4;
    border-right: 1px solid #d8dde4;
}

QFrame#topbar {
    background-color: #f5f7fa;
    border-bottom: 1px solid #d8dde4;
}

QFrame#statusbar {
    background-color: #edf0f4;
    border-top: 1px solid #d8dde4;
}


/* BRANDING */

QLabel#logo {
    color: #161b21;
    font-size: 24px;
    font-weight: 700;
}

QLabel#logo_subtitle {
    color: #7b8590;
    font-size: 10px;
}

QLabel#page_title {
    color: #161b21;
    font-size: 20px;
    font-weight: 600;
}

QLabel#page_subtitle {
    color: #727c87;
    font-size: 11px;
}


/* STATUS */

QLabel#system_status {
    color: #69747f;
    font-size: 11px;
}

QLabel#system_status_active,
QLabel#status_active {
    color: #4d725e;
    font-size: 11px;
}

QLabel#status_inactive {
    color: #7a838c;
    font-size: 11px;
}

QLabel#status_warning {
    color: #856d3f;
    font-size: 11px;
}

QLabel#status_error {
    color: #9a5555;
    font-size: 11px;
}


/* NAVIGATION */

QPushButton#nav_button {
    background-color: transparent;
    color: #66717d;
    border: none;
    border-radius: 7px;
    padding: 11px 14px;
    text-align: left;
}

QPushButton#nav_button:hover {
    background-color: #e2e6eb;
    color: #20252b;
}

QPushButton#nav_button:checked {
    background-color: #dce1e7;
    color: #161b21;
    border-left: 2px solid #7a8794;
}


/* BUTTONS */

QPushButton {
    background-color: #ffffff;
    color: #29313a;
    border: 1px solid #cbd2da;
    border-radius: 8px;
    padding: 9px 15px;
}

QPushButton:hover {
    background-color: #f0f3f6;
    border-color: #aeb8c3;
}

QPushButton:pressed {
    background-color: #e6eaee;
}

QPushButton:disabled {
    background-color: #eef0f2;
    color: #a4abb2;
    border-color: #d9dde1;
}

QPushButton#primary,
QPushButton#send {
    background-color: #e1e6eb;
    color: #161b21;
    border: 1px solid #aeb8c3;
    font-weight: 600;
}

QPushButton#primary:hover,
QPushButton#send:hover {
    background-color: #d5dbe1;
}


/* STOP */

QPushButton#stop {
    background-color: #f1e5e5;
    color: #7f4f4f;
    border: 1px solid #c9aaaa;
    font-weight: 600;
}

QPushButton#stop:hover {
    background-color: #eadada;
}


/* VOICE */

QPushButton#voice {
    background-color: #ffffff;
    color: #596570;
    border: 1px solid #cbd2da;
    border-radius: 8px;
    padding: 9px 13px;
    font-size: 15px;
}


/* CHAT */

QFrame#chat_area,
QScrollArea,
QScrollArea > QWidget > QWidget {
    background-color: #f5f7fa;
    border: none;
}


/* MESSAGE */

QFrame#message,
QFrame#message_krish {
    background-color: #ffffff;
    border: 1px solid #dce1e6;
    border-radius: 10px;
}

QFrame#message_user {
    background-color: #edf1f5;
    border: 1px solid #d5dbe1;
    border-radius: 10px;
}

QLabel#message_sender,
QLabel#message_sender_krish,
QLabel#message_sender_user {
    color: #68737e;
    font-size: 10px;
    font-weight: 700;
}

QLabel#message_text,
QLabel#message_text_krish,
QLabel#message_text_user {
    color: #252c33;
    font-size: 13px;
}


/* INPUT */

QFrame#input_bar {
    background-color: #f5f7fa;
    border-top: 1px solid #d8dde4;
}

QLineEdit,
QLineEdit#input {
    background-color: #ffffff;
    color: #20252b;
    border: 1px solid #cbd2da;
    border-radius: 9px;
    padding: 11px 14px;
    selection-background-color: #d8dee5;
}

QLineEdit:focus {
    border: 1px solid #929eaa;
}


/* TEXT EDIT */

QTextEdit {
    background-color: #ffffff;
    color: #20252b;
    border: 1px solid #cbd2da;
    border-radius: 8px;
}


/* COMBO */

QComboBox {
    background-color: #ffffff;
    color: #29313a;
    border: 1px solid #cbd2da;
    border-radius: 8px;
    padding: 8px 10px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #29313a;
    border: 1px solid #cbd2da;
    selection-background-color: #e2e6eb;
}


/* CHECKBOX */

QCheckBox {
    color: #4e5964;
    spacing: 8px;
}

QCheckBox::indicator:unchecked {
    background-color: #ffffff;
    border: 1px solid #aeb8c3;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #7c8792;
    border: 1px solid #697580;
    border-radius: 4px;
}


/* GROUP BOX */

QGroupBox {
    background-color: #ffffff;
    color: #29313a;
    border: 1px solid #d7dde3;
    border-radius: 9px;
    margin-top: 12px;
    padding: 14px;
}


/* DIALOG */

QDialog {
    background-color: #f5f7fa;
    color: #20252b;
}


/* CARDS */

QFrame#card,
QFrame#settings_section {
    background-color: #ffffff;
    border: 1px solid #d7dde3;
    border-radius: 10px;
}

QLabel#card_title {
    color: #68737e;
    font-size: 11px;
    font-weight: 600;
}

QLabel#card_value {
    color: #161b21;
    font-size: 22px;
    font-weight: 700;
}


/* PANELS */

QLabel#panel_title {
    color: #161b21;
    font-size: 18px;
    font-weight: 600;
}

QLabel#panel_description {
    color: #69747f;
    font-size: 12px;
}


/* SETTINGS */

QLabel#settings_section_title {
    color: #20252b;
    font-size: 14px;
    font-weight: 600;
}

QLabel#settings_section_description {
    color: #737e88;
    font-size: 11px;
}

QLabel#settings_item_title {
    color: #29313a;
    font-size: 13px;
    font-weight: 600;
}

QLabel#settings_item_description {
    color: #737e88;
    font-size: 11px;
}

QLabel#capability_on {
    color: #4d725e;
    font-size: 11px;
    font-weight: 600;
}

QLabel#capability_off {
    color: #7a838c;
    font-size: 11px;
}


/* SWITCH */

QPushButton#switch_off,
QPushButton#switch_on {
    min-width: 70px;
    max-width: 70px;
    min-height: 30px;
    max-height: 30px;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 11px;
    font-weight: 600;
}

QPushButton#switch_off {
    background-color: #eef0f2;
    color: #69747f;
    border: 1px solid #cbd2da;
}

QPushButton#switch_on {
    background-color: #dce9e1;
    color: #476551;
    border: 1px solid #a8bcae;
}


/* TABLES */

QTableWidget,
QTableView {
    background-color: #ffffff;
    alternate-background-color: #f5f7f9;
    color: #29313a;
    border: 1px solid #d7dde3;
    gridline-color: #e0e4e8;
    selection-background-color: #e1e6eb;
    selection-color: #20252b;
}

QHeaderView::section {
    background-color: #edf0f4;
    color: #5d6873;
    border: none;
    padding: 8px;
    font-weight: 600;
}


/* TOOLTIP */

QToolTip {
    background-color: #ffffff;
    color: #29313a;
    border: 1px solid #cbd2da;
    padding: 6px;
}


/* SCROLLBARS */

QScrollBar:vertical {
    background-color: #f5f7fa;
    width: 9px;
}

QScrollBar::handle:vertical {
    background-color: #c2c9d1;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #aeb7c0;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background-color: #f5f7fa;
    height: 9px;
}

QScrollBar::handle:horizontal {
    background-color: #c2c9d1;
    border-radius: 4px;
    min-width: 30px;
}


/* FOCUS */

QPushButton:focus,
QLineEdit:focus,
QTextEdit:focus,
QComboBox:focus {
    outline: none;
}
"""


# =============================================================
# SYSTEM THEME DETECTION
# =============================================================

def system_theme():
    """
    Detect the current operating system color scheme.

    Falls back to dark when the platform does not expose
    a usable color scheme through Qt.
    """

    app = QGuiApplication.instance()

    if app is None:
        return THEME_DARK

    try:

        scheme = app.styleHints().colorScheme()

        if scheme == Qt.ColorScheme.Light:
            return THEME_LIGHT

        if scheme == Qt.ColorScheme.Dark:
            return THEME_DARK

    except Exception:
        pass

    return THEME_DARK


# =============================================================
# EFFECTIVE THEME
# =============================================================

def effective_theme(theme):

    if theme == THEME_SYSTEM:
        return system_theme()

    if theme == THEME_LIGHT:
        return THEME_LIGHT

    if theme == THEME_DARK:
        return THEME_DARK

    return THEME_DARK


# =============================================================
# STYLESHEET
# =============================================================

def stylesheet_for(theme):

    resolved = effective_theme(theme)

    if resolved == THEME_LIGHT:
        return KRISH_LIGHT_STYLE

    return KRISH_STYLE


# =============================================================
# APPLY THEME
# =============================================================

def apply_theme(app, theme):

    if app is None:
        return THEME_DARK

    resolved = effective_theme(theme)

    app.setStyleSheet(
        stylesheet_for(theme)
    )

    app.setProperty(
        "krish_theme",
        theme,
    )

    app.setProperty(
        "krish_effective_theme",
        resolved,
    )

    return resolved


# =============================================================
# CURRENT THEME
# =============================================================

def current_theme(app=None):

    if app is None:
        app = QGuiApplication.instance()

    if app is None:
        return THEME_DARK

    theme = app.property(
        "krish_theme"
    )

    if theme in THEMES:
        return theme

    return THEME_SYSTEM


def current_effective_theme(app=None):

    if app is None:
        app = QGuiApplication.instance()

    if app is None:
        return THEME_DARK

    theme = app.property(
        "krish_effective_theme"
    )

    if theme in (
        THEME_DARK,
        THEME_LIGHT,
    ):
        return theme

    return effective_theme(
        current_theme(app)
    )