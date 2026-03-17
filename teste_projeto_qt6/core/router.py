from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QStackedWidget, QPushButton, QFrame, QLabel, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
import importlib
from core.logger import get_logger
from configs.app_config import AppConfig
import styles

logger = get_logger("Router")

class Router(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(AppConfig.DEFAULT_SCREEN["width"], AppConfig.DEFAULT_SCREEN["height"])
        self.expanded = True
        self.central_widget = QWidget(); self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget); self.main_layout.setContentsMargins(0, 0, 0, 0); self.main_layout.setSpacing(0)
        self.init_sidebar()
        self.stack = QStackedWidget(); self.main_layout.addWidget(self.stack)
        self.pages = {}
        self.apply_theme()

    def init_sidebar(self):
        self.sidebar = QFrame(); self.sidebar.setObjectName("Sidebar"); self.sidebar.setFixedWidth(240)
        self.sidebar_layout = QVBoxLayout(self.sidebar); self.sidebar_layout.setContentsMargins(10, 20, 10, 20); self.sidebar_layout.setSpacing(10)
        self.btn_toggle = QPushButton(" ☰ "); self.btn_toggle.setFixedSize(45, 45); self.btn_toggle.clicked.connect(self.toggle_sidebar); self.sidebar_layout.addWidget(self.btn_toggle)
        self.nav_buttons = []
        from configs.routes import ROUTES
        icons = ["🏠", "📂", "⚙️", "❔"]
        for i, r in enumerate(ROUTES):
            icon = icons[i] if i < len(icons) else "⚪"
            btn = QPushButton(f" {icon}   {r['label']}"); btn.setObjectName("NavButton"); btn.setFixedHeight(45); btn.setProperty("full_text", f" {icon}   {r['label']}"); btn.setProperty("icon_text", f" {icon}"); btn.clicked.connect(lambda _, p=r["path"]: self.navigate(p)); self.sidebar_layout.addWidget(btn); self.nav_buttons.append(btn)
        self.sidebar_layout.addStretch(1)
        self.theme_btn = QPushButton(AppConfig.THEME_ICONS["moon"]); self.theme_btn.setObjectName("ThemeToggle"); self.theme_btn.setFixedSize(40, 40); self.theme_btn.clicked.connect(self.toggle_theme)
        self.sidebar_layout.addWidget(self.theme_btn, 0, Qt.AlignCenter)
        self.main_layout.addWidget(self.sidebar)

    def toggle_sidebar(self):
        self.expanded = not self.expanded
        self.sidebar.setFixedWidth(240 if self.expanded else 70)
        for btn in self.nav_buttons: btn.setText(btn.property("full_text") if self.expanded else btn.property("icon_text"))

    def toggle_theme(self):
        AppConfig.DARK_MODE = not AppConfig.DARK_MODE
        self.theme_btn.setText(AppConfig.THEME_ICONS["sun"] if AppConfig.DARK_MODE else AppConfig.THEME_ICONS["moon"])
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(styles.DARK_THEME if AppConfig.DARK_MODE else styles.LIGHT_THEME)

    def navigate(self, route_path):
        from configs.routes import ROUTES
        if route_path in self.pages: self.stack.setCurrentWidget(self.pages[route_path]); return
        for r in ROUTES:
            if r["path"] == route_path:
                try:
                    module = importlib.import_module(r["module"])
                    view_class = getattr(module, r["view_class"])
                    view_instance = view_class(router=self)
                    self.stack.addWidget(view_instance); self.pages[route_path] = view_instance; self.stack.setCurrentWidget(view_instance)
                    return
                except Exception as e: logger.error(f"Erro ao carregar rota {route_path}: {e}")
