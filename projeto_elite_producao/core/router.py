from PySide6.QtWidgets import QMainWindow, QStackedWidget, QHBoxLayout, QVBoxLayout, QWidget, QFrame, QPushButton, QLabel
from PySide6.QtCore import Qt
import importlib, styles
from configs.app_config import AppConfig
from core.logger import get_logger
logger = get_logger("Router")
class Router(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(AppConfig.DEFAULT_SCREEN["width"], AppConfig.DEFAULT_SCREEN["height"])
        self.expanded = True
        self.central_widget = QWidget(); self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget); self.layout.setContentsMargins(0,0,0,0); self.layout.setSpacing(0)
        self.sidebar = QFrame(); self.sidebar.setObjectName("Sidebar"); self.sidebar.setFixedWidth(240)
        self.sidebar_layout = QVBoxLayout(self.sidebar); self.layout.addWidget(self.sidebar)
        self.stack = QStackedWidget(); self.layout.addWidget(self.stack)
        self.pages = {}
        self.init_sidebar()
        self.apply_theme()
    def init_sidebar(self):
        btn_t = QPushButton(" ☰ "); btn_t.setFixedSize(45,45); btn_t.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(btn_t)
        from configs.routes import ROUTES
        for r in ROUTES:
            btn = QPushButton(f" {r['label']}"); btn.setObjectName("NavButton"); btn.setFixedHeight(45)
            btn.clicked.connect(lambda _, p=r["path"]: self.navigate(p))
            self.sidebar_layout.addWidget(btn)
        self.sidebar_layout.addStretch(1)
        self.theme_btn = QPushButton(AppConfig.THEME_ICONS["moon"])
        self.theme_btn.clicked.connect(self.toggle_theme); self.sidebar_layout.addWidget(self.theme_btn, 0, Qt.AlignCenter)
    def toggle_sidebar(self):
        self.expanded = not self.expanded
        self.sidebar.setFixedWidth(240 if self.expanded else 70)
    def toggle_theme(self):
        AppConfig.DARK_MODE = not AppConfig.DARK_MODE
        self.theme_btn.setText(AppConfig.THEME_ICONS["sun"] if AppConfig.DARK_MODE else AppConfig.THEME_ICONS["moon"])
        self.apply_theme()
    def apply_theme(self):
        self.setStyleSheet(styles.DARK_THEME if AppConfig.DARK_MODE else styles.LIGHT_THEME)
    def navigate(self, path):
        from configs.routes import ROUTES
        if path in self.pages: self.stack.setCurrentWidget(self.pages[path]); return
        for r in ROUTES:
            if r["path"] == path:
                mod = importlib.import_module(r["module"])
                v = getattr(mod, r["view_class"])(router=self)
                self.stack.addWidget(v); self.pages[path] = v; self.stack.setCurrentWidget(v)