from pathlib import Path
import json

def init_project(project_root: Path, project_name: str = "Qt6App"):
    BASE = project_root

    def create_file(path, content=""):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content.strip(), encoding="utf-8")

    folders = [
        "assets", "core", "configs/languages", "controllers",
        "models", "views/layouts", "views/pages", "views/components",
        "data"
    ]
    for folder in folders: (BASE / folder).mkdir(parents=True, exist_ok=True)

    # --- STYLE ---
    create_file(BASE / "styles.py", """
COMMON_STYLES = \"\"\"
QCheckBox { spacing: 15px; font-size: 18px; padding: 5px; }
QCheckBox::indicator { width: 30px; height: 30px; border: 2px solid #555; border-radius: 4px; }
QCheckBox::indicator:checked { background-color: #2196F3; }
QPushButton#TextButton { background: transparent; border: none; color: #2196F3; text-decoration: underline; font-size: 14px; text-align: left; }
QPushButton#NavButton { text-align: left; padding: 12px; border: none; background: transparent; font-size: 14px; }
\"\"\"
LIGHT_THEME = COMMON_STYLES + \"\"\"
QMainWindow, QWidget { background-color: #ffffff; color: #000000; }
QFrame#Sidebar { background-color: #f0f0f0; border-right: 1px solid #cccccc; }
QPushButton#NavButton { color: #333333; }
QPushButton#NavButton:hover { background-color: #e0e0e0; }
\"\"\"
DARK_THEME = COMMON_STYLES + \"\"\"
QMainWindow, QWidget { background-color: #000000; color: #ffffff; }
QFrame#Sidebar { background-color: #1a1a1a; border-right: 1px solid #333333; }
QPushButton#NavButton { color: #ffffff; }
QPushButton#NavButton:hover { background-color: #333333; }
\"\"\"
""")

    # --- CORE ---
    create_file(BASE / "core/base_view.py", """
from PySide6.QtWidgets import QWidget, QVBoxLayout
class StatelessView(QWidget):
    def __init__(self, router=None, controller=None):
        super().__init__()
        self.router, self.controller, self.main_layout = router, controller, QVBoxLayout(self)
        self.build()
    def build(self): pass
class StatefulView(QWidget):
    def __init__(self, router=None, controller=None):
        super().__init__()
        self.router, self.controller, self.state, self.main_layout = router, controller, {}, QVBoxLayout(self)
        self.build()
    def set_state(self, **s): self.state.update(s); self.update_ui()
    def build(self): pass
    def update_ui(self): pass
""")

    create_file(BASE / "core/database.py", """
import sqlite3
from pathlib import Path
def get_connection():
    db_path = Path("data/app.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
""")

    create_file(BASE / "core/logger.py", """
import logging
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(message)s")
    return logger
""")

    create_file(BASE / "core/i18n.py", """
class I18n:
    @classmethod
    def load(cls, lang): pass
    @classmethod
    def t(cls, key): return key
""")

    create_file(BASE / "core/router.py", """
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
""")

    # --- CONFIGS ---
    create_file(BASE / "configs/app_config.py", """
class AppConfig:
    APP_NAME = \"PVRV Elite App\"
    DEFAULT_SCREEN = {"width": 1100, "height": 850}
    DARK_MODE = False
    THEME_ICONS = {"sun": "☀️", "moon": "🌙"}
""")
    create_file(BASE / "configs/routes.py", """
ROUTES = [
    {"path": "/", "view_class": "HomeView", "module": "views.pages.home_view", "label": "Home"},
    {"path": "/pdf", "view_class": "Pdf_extractorView", "module": "views.pages.pdf_extractor_view", "label": "PDF Extractor"},
    {"path": "/settings", "view_class": "SettingsView", "module": "views.pages.settings_view", "label": "Settings"},
    {"path": "/help", "view_class": "HelpView", "module": "views.pages.help_view", "label": "Help"}
]
""")
    create_file(BASE / "runtime_imports.py", """
from views.pages.home_view import HomeView
from views.pages.help_view import HelpView
from views.pages.settings_view import SettingsView
from views.pages.pdf_extractor_view import Pdf_extractorView
""")

    # --- COMPONENTS ---
    create_file(BASE / "views/components/text_button.py", """
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
class TextButton(QPushButton):
    def __init__(self, t, on_click=None, p=None):
        super().__init__(t, p); self.setObjectName('TextButton'); self.setCursor(Qt.PointingHandCursor)
        if on_click: self.clicked.connect(on_click)
""")
    
    create_file(BASE / "views/components/checklist_widget.py", """
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QFrame
class ChecklistWidget(QFrame):
    def __init__(self, md="", parent=None, on_toggle=None):
        super().__init__(parent); self.on_toggle = on_toggle; self.main_layout = QVBoxLayout(self)
        self.render_markdown(md)
    def render_markdown(self, text):
        for i in reversed(range(self.main_layout.count())):
            if self.main_layout.itemAt(i).widget(): self.main_layout.itemAt(i).widget().setParent(None)
        for line in text.strip().split("\\n"):
            c = line.strip()
            if not c: continue
            if c.startswith("## "):
                l = QLabel(c.replace("## ", "")); l.setStyleSheet("font-size: 20px; font-weight: bold;"); self.main_layout.addWidget(l)
            elif c.startswith("- ["):
                cb = QCheckBox(c[5:].strip()); cb.setChecked("[x]" in c.lower())
                cb.stateChanged.connect(lambda s, t=cb.text(): self.on_toggle(t, s == 2) if self.on_toggle else None)
                self.main_layout.addWidget(cb)
""")

    # --- PAGES ---
    create_file(BASE / "views/pages/home_view.py", """
import os, sys, subprocess
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea
from core.base_view import StatefulView
from views.components.text_button import TextButton
from views.components.checklist_widget import ChecklistWidget
from controllers.home_controller import HomeController
class HomeView(StatefulView):
    def build(self):
        self.controller = HomeController()
        banner = QFrame(); banner.setStyleSheet("background: #E3F2FD; border: 1px solid #2196F3; border-radius: 5px;")
        layout = QVBoxLayout(banner); layout.addWidget(QLabel("🚀 <b>Pronto para começar?</b>"))
        btn = TextButton("@getx-for-qt6/gemini/** (Abrir Guia)", on_click=self.open_docs)
        layout.addWidget(btn); self.main_layout.addWidget(banner)
        self.main_layout.addWidget(QLabel("<h1>🏠 Dashboard</h1>"))
        md = self.controller.load_tasks_from_db()
        self.checklist = ChecklistWidget(md, on_toggle=self.controller.update_task_status)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(self.checklist)
        self.main_layout.addWidget(scroll)
    def open_docs(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "..", "gemini"))
        if sys.platform == 'win32': os.startfile(path)
        else: subprocess.Popen(['xdg-open', path])
""")

    create_file(BASE / "views/pages/help_view.py", """
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class HelpView(StatelessView):
    def build(self): self.main_layout.addWidget(QLabel('📚 Central de Ajuda'))
""")

    create_file(BASE / "views/pages/settings_view.py", """
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class SettingsView(StatelessView):
    def build(self): self.main_layout.addWidget(QLabel('⚙️ Configurações'))
""")

    create_file(BASE / "views/pages/pdf_extractor_view.py", """
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class Pdf_extractorView(StatelessView):
    def build(self): self.main_layout.addWidget(QLabel('📄 PDF Extractor'))
""")

    # --- CONTROLLER ---
    create_file(BASE / "controllers/home_controller.py", """
from core.database import get_connection
class HomeController:
    def load_tasks_from_db(self):
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, completed INTEGER)")
        cursor.execute("SELECT title, completed FROM tasks")
        rows = cursor.fetchall()
        if not rows:
            tasks = ["Configurar Qt6", "Sidebar Responsiva", "Dark Mode Fix"]
            for t in tasks: cursor.execute("INSERT OR IGNORE INTO tasks (title, completed) VALUES (?, 0)", (t,))
            conn.commit(); cursor.execute("SELECT title, completed FROM tasks"); rows = cursor.fetchall()
        md = "## 📋 Tarefas Persistentes\\n"
        for r in rows: md += f"- [{'x' if r['completed'] else ' '}] {r['title']}\\n"
        return md
    def update_task_status(self, title, completed):
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE title = ?", (1 if completed else 0, title))
        conn.commit()
""")

    # --- ENTRY ---
    create_file(BASE / "main.py", """
import sys
from PySide6.QtWidgets import QApplication
from core.router import Router
from core.logger import get_logger
def main():
    app = QApplication(sys.argv)
    router = Router()
    router.navigate("/")
    router.show()
    get_logger("App").info("Projeto Elite Iniciado")
    sys.exit(app.exec())
if __name__ == "__main__": main()
""")

    (BASE / ".fleting").write_text("fleting-qt6-v3-elite-final", encoding="utf-8")
    print(f"✅ Template Premium V3 ELITE (Imports & Files Fix) iniciado com sucesso!")
