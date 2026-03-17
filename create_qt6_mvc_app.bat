@echo off
setlocal enabledelayedexpansion

if "%~1"=="" (
    set /p PROJECT_NAME="📂 Digite o nome do projeto [qt6_app]: "
) else (
    set PROJECT_NAME=%~1
)

if "%PROJECT_NAME%"=="" set PROJECT_NAME=qt6_app

echo 🚀 Iniciando framework PySide6 MVC (Elite Edition) em: %PROJECT_NAME%

mkdir %PROJECT_NAME%
mkdir %PROJECT_NAME%\assets
mkdir %PROJECT_NAME%\core
mkdir %PROJECT_NAME%\configs
mkdir %PROJECT_NAME%\configs\languages
mkdir %PROJECT_NAME%\controllers
mkdir %PROJECT_NAME%\models
mkdir %PROJECT_NAME%\views
mkdir %PROJECT_NAME%\views\pages
mkdir %PROJECT_NAME%\views\layouts
mkdir %PROJECT_NAME%\views\components
mkdir %PROJECT_NAME%\data
mkdir %PROJECT_NAME%\bin

:: 1. styles.py
(
echo # styles.py
echo COMMON_STYLES = """
echo QCheckBox { spacing: 15px; font-size: 18px; padding: 5px; }
echo QCheckBox::indicator { width: 30px; height: 30px; border: 2px solid #555; border-radius: 4px; }
echo QCheckBox::indicator:unchecked { background-color: transparent; }
echo QCheckBox::indicator:checked { background-color: #2196F3; }
echo QPushButton#TextButton { background-color: transparent; border: none; color: #2196F3; text-align: left; padding: 5px; font-size: 14px; text-decoration: underline; }
echo QPushButton#TextButton:hover { color: #1976D2; }
echo """
echo LIGHT_THEME = COMMON_STYLES + """
echo QMainWindow, QWidget { background-color: #ffffff; color: #000000; }
echo QFrame#Sidebar { background-color: #f0f0f0; border-right: 1px solid #cccccc; }
echo QPushButton#NavButton { text-align: left; padding: 12px; border: none; background-color: transparent; color: #333333; }
echo QPushButton#NavButton:hover { background-color: #e0e0e0; }
echo QCheckBox { color: #000000; }
echo QCheckBox::indicator { border: 2px solid #000000; }
echo """
echo DARK_THEME = COMMON_STYLES + """
echo QMainWindow, QWidget { background-color: #000000; color: #ffffff; }
echo QFrame#Sidebar { background-color: #1a1a1a; border-right: 1px solid #333333; }
echo QPushButton#NavButton { text-align: left; padding: 12px; border: none; background-color: transparent; color: #ffffff; }
echo QPushButton#NavButton:hover { background-color: #333333; }
echo QCheckBox { color: #ffffff; }
echo QCheckBox::indicator { border: 2px solid #ffffff; }
echo """
) > %PROJECT_NAME%\styles.py

:: 2. CORE: base_view.py
(
echo from PySide6.QtWidgets import QWidget, QVBoxLayout
echo class StatelessView(QWidget^):
echo     def __init__(self, router=None, controller=None^):
echo         super(StatelessView, self^).__init__(^)
echo         self.router, self.controller, self.main_layout = router, controller, QVBoxLayout(self^)
echo         self.build(^)
echo     def build(self^): pass
echo class StatefulView(QWidget^):
echo     def __init__(self, router=None, controller=None^):
echo         super(StatefulView, self^).__init__(^)
echo         self.router, self.controller, self.state, self.main_layout = router, controller, {}, QVBoxLayout(self^)
echo         self.build(^)
echo     def set_state(self, **s^): self.state.update(s^); self.update_ui(^)
echo     def build(self^): pass
echo     def update_ui(self^): pass
) > %PROJECT_NAME%\core\base_view.py

:: 3. CORE: database.py
(
echo import sqlite3
echo from pathlib import Path
echo def get_connection(^):
echo     db_path = Path("data/app.db"^)
echo     db_path.parent.mkdir(parents=True, exist_ok=True^)
echo     conn = sqlite3.connect(db_path^)
echo     conn.row_factory = sqlite3.Row
echo     return conn
) > %PROJECT_NAME%\core\database.py

:: 4. CORE: logger.py
(
echo import logging
echo def get_logger(name: str^):
echo     logger = logging.getLogger(name^)
echo     if not logger.handlers:
echo         logging.basicConfig(level=logging.INFO, format="%%(asctime)s | %%(levelname)s | %%(name)s | %%(message)s"^)
echo     return logger
) > %PROJECT_NAME%\core\logger.py

:: 5. CORE: i18n.py
(
echo import json
echo from pathlib import Path
echo class I18n:
echo     translations = {}
echo     @classmethod
echo     def load(cls, lang^):
echo         path = Path("configs/languages"^) / f"{lang}.json"
echo         if path.exists(^):
echo             with open(path, "r", encoding="utf-8"^) as f: cls.translations = json.load(f^)
echo     @classmethod
echo     def t(cls, key^):
echo         v = cls.translations
echo         for k in key.split("."^): v = v.get(k, key^)
echo         return v
) > %PROJECT_NAME%\core\i18n.py

:: 6. CORE: router.py
(
echo from PySide6.QtWidgets import (
echo     QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
echo     QStackedWidget, QPushButton, QFrame, QLabel, QSpacerItem, QSizePolicy
echo ^)
echo from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
echo import importlib
echo from core.logger import get_logger
echo from configs.app_config import AppConfig
echo import styles
echo.
echo logger = get_logger("Router"^)
echo.
echo class Router(QMainWindow^):
echo     def __init__(self^):
echo         super(Router, self^).__init__(^)
echo         self.setWindowTitle(AppConfig.APP_NAME^)
echo         self.resize(AppConfig.DEFAULT_SCREEN["width"], AppConfig.DEFAULT_SCREEN["height"]^)
echo         self.expanded = True
echo         self.central_widget = QWidget(^); self.setCentralWidget(self.central_widget^)
echo         self.main_layout = QHBoxLayout(self.central_widget^); self.main_layout.setContentsMargins(0, 0, 0, 0^); self.main_layout.setSpacing(0^)
echo         self.init_sidebar(^)
echo         self.stack = QStackedWidget(^); self.main_layout.addWidget(self.stack^)
echo         self.pages = {}
echo         self.apply_theme(^)
echo.
echo     def init_sidebar(self^):
echo         self.sidebar = QFrame(^); self.sidebar.setObjectName("Sidebar"^); self.sidebar.setFixedWidth(240^)
echo         self.sidebar_layout = QVBoxLayout(self.sidebar^); self.sidebar_layout.setContentsMargins(10, 20, 10, 20^); self.sidebar_layout.setSpacing(10^)
echo         self.btn_toggle = QPushButton(" ☰ "^); self.btn_toggle.setFixedSize(45, 45^); self.btn_toggle.clicked.connect(self.toggle_sidebar^); self.sidebar_layout.addWidget(self.btn_toggle^)
echo         self.nav_buttons = []
echo         from configs.routes import ROUTES
echo         icons = ["🏠", "📂", "⚙️", "❔"]
echo         for i, r in enumerate(ROUTES^):
echo             icon = icons[i] if i ^< len(icons^) else "⚪"
echo             btn = QPushButton(f" {icon}   {r['label']}"^); btn.setObjectName("NavButton"^); btn.setFixedHeight(45^); btn.setProperty("full_text", f" {icon}   {r['label']}"^); btn.setProperty("icon_text", f" {icon}"^); btn.clicked.connect(lambda _, p=r["path"]: self.navigate(p^)^); self.sidebar_layout.addWidget(btn^); self.nav_buttons.append(btn^)
echo         self.sidebar_layout.addStretch(1^)
echo         self.theme_btn = QPushButton(AppConfig.THEME_ICONS["moon"]^); self.theme_btn.setObjectName("ThemeToggle"^); self.theme_btn.setFixedSize(40, 40^); self.theme_btn.clicked.connect(self.toggle_theme^)
echo         self.sidebar_layout.addWidget(self.theme_btn, 0, Qt.AlignCenter^)
echo         self.main_layout.addWidget(self.sidebar^)
echo.
echo     def toggle_sidebar(self^):
echo         self.expanded = not self.expanded
echo         self.sidebar.setFixedWidth(240 if self.expanded else 70^)
echo         for btn in self.nav_buttons: btn.setText(btn.property("full_text"^) if self.expanded else btn.property("icon_text"^)^)
echo.
echo     def toggle_theme(self^):
echo         AppConfig.DARK_MODE = not AppConfig.DARK_MODE
echo         self.theme_btn.setText(AppConfig.THEME_ICONS["sun"] if AppConfig.DARK_MODE else AppConfig.THEME_ICONS["moon"]^)
echo         self.apply_theme(^)
echo.
echo     def apply_theme(self^):
echo         self.setStyleSheet(styles.DARK_THEME if AppConfig.DARK_MODE else styles.LIGHT_THEME^)
echo.
echo     def navigate(self, route_path^):
echo         from configs.routes import ROUTES
echo         if route_path in self.pages: self.stack.setCurrentWidget(self.pages[route_path]^); return
echo         for r in ROUTES:
echo             if r["path"] == route_path:
echo                 try:
echo                     module = importlib.import_module(r["module"]^)
echo                     view_class = getattr(module, r["view_class"]^)
echo                     view_instance = view_class(router=self^)
echo                     self.stack.addWidget(view_instance^); self.pages[route_path] = view_instance^; self.stack.setCurrentWidget(view_instance^)
echo                     return
echo                 except Exception as e: logger.error(f"Erro ao carregar rota {route_path}: {e}"^)
) > %PROJECT_NAME%\coreouter.py

:: 7. CONFIGS: app_config.py
(
echo class AppConfig:
echo     APP_NAME = "PVRV Advanced Desktop"
echo     DEFAULT_SCREEN = {"width": 1100, "height": 850}
echo     DARK_MODE = False
echo     THEME_ICONS = {"sun": "☀️", "moon": "🌙"}
) > %PROJECT_NAME%\configs\app_config.py

:: 8. CONFIGS: routes.py
(
echo ROUTES = [
echo     { "path": "/", "view_class": "HomeView", "module": "views.pages.home_view", "label": "Home" },
echo     { "path": "/pdf_extractor", "view_class": "Pdf_extractorView", "module": "views.pages.pdf_extractor_view", "label": "PDF Extractor" },
echo     { "path": "/settings", "view_class": "SettingsView", "module": "views.pages.settings_view", "label": "Configurações" },
echo     { "path": "/help", "view_class": "HelpView", "module": "views.pages.help_view", "label": "Ajuda" },
echo ]
) > %PROJECT_NAME%\configsoutes.py

:: 9. runtime_imports.py
(
echo from views.pages.home_view import HomeView
echo from views.pages.help_view import HelpView
echo from views.pages.settings_view import SettingsView
echo from views.pages.pdf_extractor_view import Pdf_extractorView
) > %PROJECT_NAME%untime_imports.py

:: 10. main.py
(
echo import sys
echo from PySide6.QtWidgets import QApplication
echo from core.logger import get_logger
echo import runtime_imports 
echo logger = get_logger("App"^)
echo def main(^):
echo     app = QApplication(sys.argv^)
echo     try:
echo         from core.i18n import I18n
echo         I18n.load("pt"^)
echo         from core.router import Router
echo         router = Router(^)
echo         router.navigate("/"^)
echo         router.show(^)
echo         logger.info("Aplicação Desktop PVRV iniciada com sucesso"^)
echo         sys.exit(app.exec(^)^)
echo     except Exception as e: print(f"Erro Crítico no Boot: {e}"^)
echo if __name__ == "__main__": main(^)
) > %PROJECT_NAME%\main.py

:: 11. views/components/text_button.py
(
echo from PySide6.QtWidgets import QPushButton
echo from PySide6.QtCore import Qt
echo class TextButton(QPushButton^):
echo     def __init__(self, text, on_click=None, parent=None^):
echo         super(TextButton, self^).__init__(text, parent^)
echo         self.setObjectName("TextButton"^); self.setCursor(Qt.PointingHandCursor^)
echo         if on_click: self.clicked.connect(on_click^)
) > %PROJECT_NAME%\views\components	ext_button.py

:: 12. views/components/checklist_widget.py
(
echo from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QFrame
echo from PySide6.QtCore import Qt
echo class ChecklistWidget(QFrame^):
echo     def __init__(self, markdown_text="", parent=None, on_toggle=None^):
echo         super(ChecklistWidget, self^).__init__(parent^); self.on_toggle = on_toggle; self.main_layout = QVBoxLayout(self^); self.main_layout.setSpacing(15^); self.main_layout.setContentsMargins(15, 15, 15, 15^); self.render_markdown(markdown_text^)
echo     def render_markdown(self, text^):
echo         for i in reversed(range(self.main_layout.count(^)^)^):
echo             item = self.main_layout.itemAt(i^)
echo             if item.widget(^): item.widget(^).setParent(None^)
echo         lines = text.strip(^).split("
"^)
echo         for line in lines:
echo             content = line.strip(^)
echo             if not content: continue
echo             if content.startswith("## "^):
echo                 header = QLabel(content.replace("## ", ""^)^); header.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px;"^); self.main_layout.addWidget(header^)
echo             elif content.startswith("- ["^):
echo                 checkbox = QCheckBox(content[5:].strip(^)^); checkbox.setChecked("[x]" in content.lower(^)^)
echo                 checkbox.stateChanged.connect(lambda state, t=checkbox.text(^): self.on_toggle(t, state == 2^) if self.on_toggle else None^)
echo                 if line.startswith("  "^): checkbox.setStyleSheet("margin-left: 35px;"^)
echo                 self.main_layout.addWidget(checkbox^)
) > %PROJECT_NAME%\views\components\checklist_widget.py

:: 13. controllers/home_controller.py
(
echo from PySide6.QtCore import QObject
echo from core.database import get_connection
echo class HomeController(QObject^):
echo     def __init__(self^): super(HomeController, self^).__init__(^)
echo     def get_welcome_message(self, name^): return f"Olá, {name}. Prazer em conhecer você! 👋" if name else "Por favor, digite seu nome acima."
echo     def load_tasks_from_db(self^):
echo         conn = get_connection(^); cursor = conn.cursor(^)
echo         cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, completed INTEGER^)"^)
echo         cursor.execute("SELECT title, completed FROM tasks"^)
echo         rows = cursor.fetchall(^)
echo         if not rows:
echo             self.seed_initial_tasks(^)
echo             cursor.execute("SELECT title, completed FROM tasks"^); rows = cursor.fetchall(^)
echo         md = "## 📋 Minhas Tarefas (DB Persistente)
"
echo         for row in rows: md += f"- [{'x' if row['completed'] == 1 else ' '}] {row['title']}
"
echo         return md
echo     def update_task_status(self, title, completed^):
echo         conn = get_connection(^); cursor = conn.cursor(^); cursor.execute("UPDATE tasks SET completed = ? WHERE title = ?", (1 if completed else 0, title^)^); conn.commit(^)
echo     def seed_initial_tasks(self^):
echo         tasks = ["Configurar PySide6 MVC", "Criar Sidebar Responsiva", "Implementar Loader Palkia", "Finalizar Dark Mode Fix"]
echo conn = get_connection(^); cursor = conn.cursor(^)
echo for t in tasks: cursor.execute("INSERT OR IGNORE INTO tasks (title, completed) VALUES (?, 0)", (t,^)^)
echo conn.commit(^)
) > %PROJECT_NAME%\controllers\home_controller.py

:: 14. views/pages/home_view.py
(
echo import os, sys, subprocess
echo from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QFrame^)
echo from core.base_view import StatefulView
echo from controllers.home_controller import HomeController
echo from views.components.checklist_widget import ChecklistWidget
echo from views.components.text_button import TextButton
echo from core.i18n import I18n
echo class HomeView(StatefulView^):
echo     def __init__(self, router=None^): super(HomeView, self^).__init__(router=router, controller=HomeController(^)^)
echo     def build(self^):
echo         doc_frame = QFrame(^); doc_frame.setStyleSheet("background-color: #E3F2FD; border-radius: 5px; border: 1px solid #2196F3;"^); doc_layout = QVBoxLayout(doc_frame^)
echo         doc_layout.addWidget(QLabel("💡 <b>Dica de Elite:</b> Leia a documentação técnica para começar:"^)^)
echo         self.btn_gemini = TextButton("@getx-for-qt6/gemini/** (Abrir Guia no Explorador)", on_click=self.open_gemini_docs^); doc_layout.addWidget(self.btn_gemini^); self.main_layout.addWidget(doc_frame^)
echo         self.welcome_label = QLabel(I18n.t("home.welcome"^)^); self.welcome_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-top: 10px;"^); self.main_layout.addWidget(self.welcome_label^)
echo         interaction_layout = QHBoxLayout(^); self.name_input = QLineEdit(^); self.name_input.setPlaceholderText("Seu nome..."^); interaction_layout.addWidget(self.name_input, 3^)
echo         self.btn_greet = QPushButton("🚀"^); self.btn_greet.setFixedSize(50, 50^); self.btn_greet.clicked.connect(self.on_greet_click^); interaction_layout.addWidget(self.btn_greet^); self.main_layout.addLayout(interaction_layout^)
echo         self.greeting_display = QLabel("Olá!"^); self.main_layout.addWidget(self.greeting_display^)
echo         md_content = self.controller.load_tasks_from_db(^); self.checklist = ChecklistWidget(md_content, on_toggle=self.on_task_toggled^)
echo         scroll = QScrollArea(^); scroll.setWidgetResizable(True^); scroll.setWidget(self.checklist^); self.main_layout.addWidget(scroll^)
echo     def open_gemini_docs(self^):
echo         path = os.path.abspath(os.path.join(os.getcwd(^), "..", "gemini"^)^)
echo         if sys.platform == 'win32': os.startfile(path^)
echo         else: subprocess.Popen(['xdg-open', path]^)
echo     def on_task_toggled(self, title, completed^): self.controller.update_task_status(title, completed^)
echo     def on_greet_click(self^): self.greeting_display.setText(self.controller.get_welcome_message(self.name_input.text(^)^)^)
) > %PROJECT_NAME%\views\pages\home_view.py

:: 15. views/pages/help_view.py
(
echo from PySide6.QtWidgets import QLabel
echo from core.base_view import StatelessView
echo class HelpView(StatelessView^):
echo     def build(self^):
echo         label = QLabel("📚 Central de Ajuda. Aqui você encontra os guias de uso."^); label.setStyleSheet("font-size: 20px;"^); self.main_layout.addWidget(label^)
) > %PROJECT_NAME%\views\pages\help_view.py

:: 16. views/pages/settings_view.py
(
echo from PySide6.QtWidgets import QLabel
echo from core.base_view import StatelessView
echo class SettingsView(StatelessView^):
echo     def build(self^):
echo         label = QLabel("⚙️ Configurações do Sistema. Ajuste as preferências do framework."^); label.setStyleSheet("font-size: 20px;"^); self.main_layout.addWidget(label^)
) > %PROJECT_NAME%\views\pages\settings_view.py

:: 17. views/pages/pdf_extractor_view.py
(
echo from PySide6.QtWidgets import QLabel
echo from core.base_view import StatelessView
echo class Pdf_extractorView(StatelessView^):
echo     def build(self^):
echo         label = QLabel("📄 Extrator de PDF Palkia. ETL de PDFs integrada."^); label.setStyleSheet("font-size: 20px;"^); self.main_layout.addWidget(label^)
) > %PROJECT_NAME%\views\pages\pdf_extractor_view.py

:: 18. configs/languages/pt.json
(
echo {"home": {"welcome": "Painel de Controle PVRV"}}
) > %PROJECT_NAME%\configs\languages\pt.json

:: 19. .fleting
echo fleting-qt6-v3-elite-literal > %PROJECT_NAME%\.fleting

echo ✅ Framework Elite Edition gerado com sucesso em %PROJECT_NAME%
echo 👉 Para rodar: cd %PROJECT_NAME% ^&^& python main.py
