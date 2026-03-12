from pathlib import Path
import json

def init_project(project_root: Path, project_name: str = "Qt6App"):
    BASE = project_root

    def create_file(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content.strip(), encoding="utf-8")

    # Estrutura de Pastas
    for folder in ["assets", "core", "configs/languages", "controllers", "models", "views/layouts", "views/pages", "views/components", "data"]:
        (BASE / folder).mkdir(parents=True, exist_ok=True)

    # --- DICIONÁRIO DE TEMPLATES LITERAIS ---
    
    TEMPLATES = {
        "styles.py": """
# styles.py
COMMON_STYLES = \"\"\"
QCheckBox { spacing: 15px; font-size: 18px; padding: 5px; }
QCheckBox::indicator { width: 30px; height: 30px; border: 2px solid #555; border-radius: 4px; }
QCheckBox::indicator:unchecked { background-color: transparent; }
QCheckBox::indicator:checked { background-color: #2196F3; }
QPushButton#TextButton { background-color: transparent; border: none; color: #2196F3; text-align: left; padding: 5px; font-size: 14px; text-decoration: underline; }
QPushButton#TextButton:hover { color: #1976D2; }
\"\"\"
LIGHT_THEME = COMMON_STYLES + \"\"\"
QMainWindow, QWidget { background-color: #ffffff; color: #000000; }
QFrame#Sidebar { background-color: #f0f0f0; border-right: 1px solid #cccccc; }
QPushButton#NavButton { text-align: left; padding: 12px; border: none; background-color: transparent; color: #333333; }
QPushButton#NavButton:hover { background-color: #e0e0e0; }
QCheckBox { color: #000000; }
QCheckBox::indicator { border: 2px solid #000000; }
\"\"\"
DARK_THEME = COMMON_STYLES + \"\"\"
QMainWindow, QWidget { background-color: #000000; color: #ffffff; }
QFrame#Sidebar { background-color: #1a1a1a; border-right: 1px solid #333333; }
QPushButton#NavButton { text-align: left; padding: 12px; border: none; background-color: transparent; color: #ffffff; }
QPushButton#NavButton:hover { background-color: #333333; }
QCheckBox { color: #ffffff; }
QCheckBox::indicator { border: 2px solid #ffffff; }
\"\"\"
""",
        "core/base_view.py": """
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
""",
        "core/database.py": """
import sqlite3
from pathlib import Path
def get_connection():
    db_path = Path("data/app.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
""",
        "core/logger.py": """
import logging
def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    return logger
""",
        "core/i18n.py": """
import json
from pathlib import Path
class I18n:
    translations = {}
    @classmethod
    def load(cls, lang):
        path = Path("configs/languages") / f"{lang}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f: cls.translations = json.load(f)
    @classmethod
    def t(cls, key):
        v = cls.translations
        for k in key.split("."): v = v.get(k, key)
        return v
""",
        "core/router.py": """
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
""",
        "configs/app_config.py": """
class AppConfig:
    APP_NAME = "PVRV Advanced Desktop"
    DEFAULT_SCREEN = {"width": 1100, "height": 850}
    DARK_MODE = False
    THEME_ICONS = {"sun": "☀️", "moon": "🌙"}
""",
        "configs/routes.py": """
ROUTES = [
    { "path": "/", "view_class": "HomeView", "module": "views.pages.home_view", "label": "Home" },
    { "path": "/pdf_extractor", "view_class": "Pdf_extractorView", "module": "views.pages.pdf_extractor_view", "label": "PDF Extractor" },
    { "path": "/settings", "view_class": "SettingsView", "module": "views.pages.settings_view", "label": "Configurações" },
    { "path": "/help", "view_class": "HelpView", "module": "views.pages.help_view", "label": "Ajuda" },
]
""",
        "runtime_imports.py": """
from views.pages.home_view import HomeView
from views.pages.help_view import HelpView
from views.pages.settings_view import SettingsView
from views.pages.pdf_extractor_view import Pdf_extractorView
""",
        "main.py": """
import sys
from PySide6.QtWidgets import QApplication
from core.logger import get_logger
import runtime_imports 
logger = get_logger("App")
def main():
    app = QApplication(sys.argv)
    try:
        from core.i18n import I18n
        I18n.load("pt")
        from core.router import Router
        router = Router()
        router.navigate("/")
        router.show()
        logger.info("Aplicação Desktop PVRV iniciada com sucesso")
        sys.exit(app.exec())
    except Exception as e: print(f"Erro Crítico no Boot: {e}")
if __name__ == "__main__": main()
""",
        "views/components/text_button.py": """
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
class TextButton(QPushButton):
    def __init__(self, text, on_click=None, parent=None):
        super().__init__(text, parent)
        self.setObjectName("TextButton"); self.setCursor(Qt.PointingHandCursor)
        if on_click: self.clicked.connect(on_click)
""",
        "views/components/checklist_widget.py": """
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QFrame
from PySide6.QtCore import Qt
class ChecklistWidget(QFrame):
    def __init__(self, markdown_text="", parent=None, on_toggle=None):
        super().__init__(parent); self.on_toggle = on_toggle; self.main_layout = QVBoxLayout(self); self.main_layout.setSpacing(15); self.main_layout.setContentsMargins(15, 15, 15, 15); self.render_markdown(markdown_text)
    def render_markdown(self, text):
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            if item.widget(): item.widget().setParent(None)
        lines = text.strip().split("\\n")
        for line in lines:
            content = line.strip()
            if not content: continue
            if content.startswith("## "):
                header = QLabel(content.replace("## ", "")); header.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px;"); self.main_layout.addWidget(header)
            elif content.startswith("- ["):
                checkbox = QCheckBox(content[5:].strip()); checkbox.setChecked("[x]" in content.lower())
                checkbox.stateChanged.connect(lambda state, t=checkbox.text(): self.on_toggle(t, state == 2) if self.on_toggle else None)
                if line.startswith("  "): checkbox.setStyleSheet("margin-left: 35px;")
                self.main_layout.addWidget(checkbox)
""",
        "controllers/home_controller.py": """
from PySide6.QtCore import QObject
from core.database import get_connection
class HomeController(QObject):
    def __init__(self): super().__init__()
    def get_welcome_message(self, name): return f"Olá, {name}. Prazer em conhecer você! 👋" if name else "Por favor, digite seu nome acima."
    def load_tasks_from_db(self):
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, completed INTEGER)")
        cursor.execute("SELECT title, completed FROM tasks")
        rows = cursor.fetchall()
        if not rows:
            self.seed_initial_tasks()
            cursor.execute("SELECT title, completed FROM tasks"); rows = cursor.fetchall()
        md = "## 📋 Minhas Tarefas (DB Persistente)\\n"
        for row in rows: md += f"- [{'x' if row['completed'] == 1 else ' '}] {row['title']}\\n"
        return md
    def update_task_status(self, title, completed):
        conn = get_connection(); cursor = conn.cursor(); cursor.execute("UPDATE tasks SET completed = ? WHERE title = ?", (1 if completed else 0, title)); conn.commit()
    def seed_initial_tasks(self):
        tasks = ["Configurar PySide6 MVC", "Criar Sidebar Responsiva", "Implementar Loader Palkia", "Finalizar Dark Mode Fix"]
        conn = get_connection(); cursor = conn.cursor()
        for t in tasks: cursor.execute("INSERT OR IGNORE INTO tasks (title, completed) VALUES (?, 0)", (t,))
        conn.commit()
""",
        "views/pages/home_view.py": """
import os, sys, subprocess
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QFrame)
from core.base_view import StatefulView
from controllers.home_controller import HomeController
from views.components.checklist_widget import ChecklistWidget
from views.components.text_button import TextButton
from core.i18n import I18n
class HomeView(StatefulView):
    def __init__(self, router=None): super().__init__(router=router, controller=HomeController())
    def build(self):
        doc_frame = QFrame(); doc_frame.setStyleSheet("background-color: #E3F2FD; border-radius: 5px; border: 1px solid #2196F3;"); doc_layout = QVBoxLayout(doc_frame)
        doc_layout.addWidget(QLabel("💡 <b>Dica de Elite:</b> Leia a documentação técnica para começar:"))
        self.btn_gemini = TextButton("@getx-for-qt6/gemini/** (Abrir Guia no Explorador)", on_click=self.open_gemini_docs); doc_layout.addWidget(self.btn_gemini); self.main_layout.addWidget(doc_frame)
        self.welcome_label = QLabel(I18n.t("home.welcome")); self.welcome_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-top: 10px;"); self.main_layout.addWidget(self.welcome_label)
        interaction_layout = QHBoxLayout(); self.name_input = QLineEdit(); self.name_input.setPlaceholderText("Seu nome..."); interaction_layout.addWidget(self.name_input, 3)
        self.btn_greet = QPushButton("🚀"); self.btn_greet.setFixedSize(50, 50); self.btn_greet.clicked.connect(self.on_greet_click); interaction_layout.addWidget(self.btn_greet); self.main_layout.addLayout(interaction_layout)
        self.greeting_display = QLabel("Olá!"); self.main_layout.addWidget(self.greeting_display)
        md_content = self.controller.load_tasks_from_db(); self.checklist = ChecklistWidget(md_content, on_toggle=self.on_task_toggled)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(self.checklist); self.main_layout.addWidget(scroll)
    def open_gemini_docs(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "..", "gemini"))
        if sys.platform == 'win32': os.startfile(path)
        else: subprocess.Popen(['xdg-open', path])
    def on_task_toggled(self, title, completed): self.controller.update_task_status(title, completed)
    def on_greet_click(self): self.greeting_display.setText(self.controller.get_welcome_message(self.name_input.text()))
""",
        "views/pages/help_view.py": """
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class HelpView(StatelessView):
    def build(self):
        label = QLabel("📚 Central de Ajuda. Aqui você encontra os guias de uso."); label.setStyleSheet("font-size: 20px;"); self.main_layout.addWidget(label)
""",
        "views/pages/settings_view.py": """
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class SettingsView(StatelessView):
    def build(self):
        label = QLabel("⚙️ Configurações do Sistema. Ajuste as preferências do framework."); label.setStyleSheet("font-size: 20px;"); self.main_layout.addWidget(label)
""",
        "views/pages/pdf_extractor_view.py": """
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class Pdf_extractorView(StatelessView):
    def build(self):
        label = QLabel("📄 Extrator de PDF Palkia. ETL de PDFs integrada."); label.setStyleSheet("font-size: 20px;"); self.main_layout.addWidget(label)
"""
    }

    for file_path, content in TEMPLATES.items():
        create_file(BASE / file_path, content)

    # Outros arquivos fixos
    create_file(BASE / "configs/languages/pt.json", '{"home": {"welcome": "Painel de Controle PVRV"}}')
    (BASE / ".fleting").write_text("fleting-qt6-v3-elite-literal", encoding="utf-8")
    print(f"✅ Template Premium V3 ELITE LITERAL iniciado com sucesso!")
