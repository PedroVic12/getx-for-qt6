import sys
import os
from pathlib import Path

def create_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_project(project_name, template_type):
    project_name_clean = project_name.replace("-", "_")
    base = Path(project_name)
    base.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Gerando projeto '{project_name}' usando o Template {template_type}...")

    if template_type == 1:
        # ==========================================
        # 1. PySide6 MVC (Widgets)
        # ==========================================
        view_class_name = project_name_clean.capitalize() + "View"
        view_file_name = f"{project_name_clean}_view"

        # Pastas
        for folder in ["assets", "core", "configs/languages", "controllers", "models", "views/pages", "views/layouts", "views/components", "data", "bin"]:
            (base / folder).mkdir(parents=True, exist_ok=True)

        # styles.py
        create_file(base / "styles.py", """
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
""")

        # base_view.py
        create_file(base / "core/base_view.py", """
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

        # database.py
        create_file(base / "core/database.py", """
import sqlite3
from pathlib import Path
def get_connection():
    db_path = Path("data/app.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
""")

        # logger.py
        create_file(base / "core/logger.py", """
import logging
def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    return logger
""")

        # i18n.py
        create_file(base / "core/i18n.py", """
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
""")

        # router.py
        create_file(base / "core/router.py", f"""
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
        self.pages = {{}}
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
            btn = QPushButton(f" {{icon}}   {{r['label']}}"); btn.setObjectName("NavButton"); btn.setFixedHeight(45); btn.setProperty("full_text", f" {{icon}}   {{r['label']}}"); btn.setProperty("icon_text", f" {{icon}}"); btn.clicked.connect(lambda _, p=r["path"]: self.navigate(p)); self.sidebar_layout.addWidget(btn); self.nav_buttons.append(btn)
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
                except Exception as e: logger.error(f"Erro ao carregar rota {{route_path}}: {{e}}")
""")

        # app_config.py
        create_file(base / "configs/app_config.py", f"""
class AppConfig:
    APP_NAME = "{project_name}"
    DEFAULT_SCREEN = {{"width": 1100, "height": 850}}
    DARK_MODE = False
    THEME_ICONS = {{"sun": "☀️", "moon": "🌙"}}
""")

        # routes.py
        create_file(base / "configs/routes.py", f"""
ROUTES = [
    {{ "path": "/", "view_class": "HomeView", "module": "views.pages.home_view", "label": "Home" }},
    {{ "path": "/app_view", "view_class": "{view_class_name}", "module": "views.pages.{view_file_name}", "label": "Main View" }},
    {{ "path": "/settings", "view_class": "SettingsView", "module": "views.pages.settings_view", "label": "Configurações" }},
    {{ "path": "/help", "view_class": "HelpView", "module": "views.pages.help_view", "label": "Ajuda" }},
]
""")

        # runtime_imports.py
        create_file(base / "runtime_imports.py", f"""
from views.pages.home_view import HomeView
from views.pages.help_view import HelpView
from views.pages.settings_view import SettingsView
from views.pages.{view_file_name} import {view_class_name}
""")

        # main.py
        create_file(base / "main.py", """
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
        logger.info("Aplicação Desktop iniciada com sucesso")
        sys.exit(app.exec())
    except Exception as e: print(f"Erro Crítico no Boot: {e}")
if __name__ == "__main__": main()
""")

        # text_button.py
        create_file(base / "views/components/text_button.py", """
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
class TextButton(QPushButton):
    def __init__(self, text, on_click=None, parent=None):
        super().__init__(text, parent)
        self.setObjectName("TextButton"); self.setCursor(Qt.PointingHandCursor)
        if on_click: self.clicked.connect(on_click)
""")

        # checklist_widget.py
        create_file(base / "views/components/checklist_widget.py", """
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QFrame
from PySide6.QtCore import Qt
class ChecklistWidget(QFrame):
    def __init__(self, markdown_text="", parent=None, on_toggle=None):
        super().__init__(parent); self.on_toggle = on_toggle; self.main_layout = QVBoxLayout(self); self.main_layout.setSpacing(15); self.main_layout.setContentsMargins(15, 15, 15, 15); self.render_markdown(markdown_text)
    def render_markdown(self, text):
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            if item.widget(): item.widget().setParent(None)
        lines = text.strip().split("\n")
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
""")

        # home_controller.py
        create_file(base / "controllers/home_controller.py", """
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
        md = "## 📋 Minhas Tarefas (DB Persistente)\n"
        for row in rows: md += f"- [{'x' if row['completed'] == 1 else ' '}] {row['title']}\n"
        return md
    def update_task_status(self, title, completed):
        conn = get_connection(); cursor = conn.cursor(); cursor.execute("UPDATE tasks SET completed = ? WHERE title = ?", (1 if completed else 0, title)); conn.commit()
    def seed_initial_tasks(self):
        tasks = ["Configurar PySide6 MVC", "Criar Sidebar Responsiva", "Finalizar Dark Mode Fix"]
        conn = get_connection(); cursor = conn.cursor()
        for t in tasks: cursor.execute("INSERT OR IGNORE INTO tasks (title, completed) VALUES (?, 0)", (t,))
        conn.commit()
""")

        # home_view.py
        create_file(base / "views/pages/home_view.py", """
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
        doc_layout.addWidget(QLabel("💡 <b>Dica:</b> Comece editando este arquivo."))
        self.btn_gemini = TextButton("@getx-for-qt6/gemini/** (Abrir Guia)", on_click=self.open_gemini_docs); doc_layout.addWidget(self.btn_gemini); self.main_layout.addWidget(doc_frame)
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
""")

        # help_view.py
        create_file(base / "views/pages/help_view.py", """
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class HelpView(StatelessView):
    def build(self):
        label = QLabel("📚 Central de Ajuda."); label.setStyleSheet("font-size: 20px;"); self.main_layout.addWidget(label)
""")

        # settings_view.py
        create_file(base / "views/pages/settings_view.py", """
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class SettingsView(StatelessView):
    def build(self):
        label = QLabel("⚙️ Configurações do Sistema."); label.setStyleSheet("font-size: 20px;"); self.main_layout.addWidget(label)
""")

        # custom page view
        create_file(base / f"views/pages/{view_file_name}.py", f"""
from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class {view_class_name}(StatelessView):
    def build(self):
        label = QLabel("📄 View Principal do projeto: {project_name}"); label.setStyleSheet("font-size: 20px;"); self.main_layout.addWidget(label)
""")

        # pt.json
        create_file(base / "configs/languages/pt.json", f'{{"home": {{"welcome": "Painel de Controle {project_name}"}}}}')
        # .fleting
        create_file(base / ".fleting", "fleting-qt6-v3-elite-literal")

        print(f"✅ Framework Elite Edition gerado com sucesso em {project_name}")
        print(f"👉 Para rodar: cd {project_name} && python3 main.py")

    elif template_type == 2:
        # ==========================================
        # 2. PySide6 Qt Quick (QML)
        # ==========================================
        for folder in ["controllers", "models", "views"]:
            (base / folder).mkdir(parents=True, exist_ok=True)

        create_file(base / "main.py", """
import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Property, Signal

class MainController(QObject):
    nameChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self._name = "Pedro"

    @Property(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._name != value:
            self._name = value
            self.nameChanged.emit(value)

    @Slot(str)
    def greet(self, user_name):
        print(f"Olá do Python para {user_name}!")
        self.name = user_name

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    controller = MainController()
    engine.rootContext().setContextProperty("controller", controller)

    qml_file = os.path.join(os.path.dirname(__file__), 'views', 'main.qml')
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    print("Aplicação Qt Quick iniciada com sucesso!")
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
""")

        create_file(base / "views/main.qml", f"""
import QtQuick
import QtQuick.Controls

ApplicationWindow {{
    visible: true
    width: 600
    height: 450
    title: "Batcaverna - Qt Quick App ({project_name})"

    background: Rectangle {{
        color: "#1e1e2e"
    }}

    Column {{
        anchors.centerIn: parent
        spacing: 20

        Text {{
            text: "Bem-vindo ao Qt Quick (QML)!"
            font.pixelSize: 24
            font.bold: true
            color: "#cdd6f4"
            anchors.horizontalCenter: parent.horizontalCenter
        }}

        Text {{
            text: "Nome atual no Controller: " + controller.name
            font.pixelSize: 16
            color: "#a6adc8"
            anchors.horizontalCenter: parent.horizontalCenter
        }}

        TextField {{
            id: nameInput
            placeholderText: "Digite seu nome..."
            color: "#cdd6f4"
            anchors.horizontalCenter: parent.horizontalCenter
            background: Rectangle {{
                implicitWidth: 200
                implicitHeight: 40
                color: "#313244"
                radius: 6
            }}
        }}

        Button {{
            text: "Enviar para Python"
            anchors.horizontalCenter: parent.horizontalCenter
            contentItem: Text {{
                text: parent.text
                color: "#11111b"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
            }}
            background: Rectangle {{
                implicitWidth: 150
                implicitHeight: 40
                color: parent.down ? "#a6e3a1" : "#89b4fa"
                radius: 8
            }}
            onClicked: {{
                controller.greet(nameInput.text)
            }}
        }}
    }}
}}
""")

        print(f"✅ Projeto Qt Quick (QML) gerado em {project_name}")
        print(f"👉 Para rodar: cd {project_name} && python3 main.py")

    elif template_type == 3:
        # ==========================================
        # 3. PySide6 Qt Designer (.ui)
        # ==========================================
        for folder in ["views"]:
            (base / folder).mkdir(parents=True, exist_ok=True)

        create_file(base / "main.py", """
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MainWindow(QMainWindow):
    def __init__(self, ui_file_path):
        super().__init__()
        loader = QUiLoader()
        file = QFile(ui_file_path)
        if not file.open(QFile.ReadOnly):
            print(f"Não foi possível abrir o arquivo UI: {ui_file_path}")
            sys.exit(-1)
        self.ui = loader.load(file, self)
        file.close()
        
        self.setCentralWidget(self.ui.centralWidget())
        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.size())
        self.setStyleSheet(self.ui.styleSheet())

        # Conectar widgets da UI
        self.btn_click = self.ui.findChild(QPushButton, "btn_click")
        self.lbl_title = self.ui.findChild(QLabel, "lbl_title")
        self.txt_input = self.ui.findChild(QLineEdit, "txt_input")

        if self.btn_click:
            self.btn_click.clicked.connect(self.on_btn_click)

    def on_btn_click(self):
        text = self.txt_input.text() if self.txt_input else ""
        if text:
            self.lbl_title.setText(f"Texto recebido: {text}")
        else:
            self.lbl_title.setText("Por favor, digite algo!")

def main():
    app = QApplication(sys.argv)
    
    ui_path = os.path.join(os.path.dirname(__file__), 'views', 'mainwindow.ui')
    window = MainWindow(ui_path)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
""")

        create_file(base / "views/mainwindow.ui", """
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>500</width>
    <height>350</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Batcaverna - Qt Designer UI</string>
  </property>
  <property name="styleSheet">
   <string notr="true">QMainWindow { background-color: #1e1e2e; } QLabel { color: #cdd6f4; font-size: 16px; } QPushButton { background-color: #89b4fa; color: #11111b; border-radius: 6px; padding: 8px 16px; font-weight: bold; } QPushButton:hover { background-color: #b4befe; } QLineEdit { background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; border-radius: 6px; padding: 8px; }</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLabel" name="lbl_title">
      <property name="text">
       <string>Interface carregada via arquivo .ui!</string>
      </property>
      <property name="alignment">
       <set>Qt::AlignCenter</set>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLineEdit" name="txt_input">
      <property name="placeholderText">
       <string>Escreva algo...</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="btn_click">
      <property name="text">
       <string>Executar Ação</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
""")

        print(f"✅ Projeto Qt Designer (.ui) gerado em {project_name}")
        print(f"👉 Para rodar: cd {project_name} && python3 main.py")

    elif template_type == 4:
        # ==========================================
        # 4. C++ Qt Quick (QML + CMake)
        # ==========================================
        for folder in ["src", "views"]:
            (base / folder).mkdir(parents=True, exist_ok=True)

        create_file(base / "CMakeLists.txt", f"""
cmake_minimum_required(VERSION 3.16)
project(cpp_qml_app VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick)

add_executable(cpp_qml_app
    src/main.cpp
    src/SampleController.h
    src/SampleController.cpp
)

target_link_libraries(cpp_qml_app PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
)

file(COPY views/main.qml DESTINATION ${{CMAKE_CURRENT_BINARY_DIR}}/views)
""")

        create_file(base / "src/SampleController.h", """
#pragma once
#include <QObject>
#include <QString>

class SampleController : public QObject {
    Q_OBJECT
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)

public:
    explicit SampleController(QObject *parent = nullptr);

    QString name() const;
    void setName(const QString &newName);

    Q_INVOKABLE void greet(const QString &userName);

signals:
    void nameChanged(const QString &newName);

private:
    QString m_name;
};
""")

        create_file(base / "src/SampleController.cpp", """
#include "SampleController.h"
#include <QDebug>

SampleController::SampleController(QObject *parent)
    : QObject(parent), m_name("Pedro") {}

QString SampleController::name() const {
    return m_name;
}

void SampleController::setName(const QString &newName) {
    if (m_name != newName) {
        m_name = newName;
        emit nameChanged(m_name);
    }
}

void SampleController::greet(const QString &userName) {
    qDebug() << "Olá do C++ para" << userName;
    setName(userName);
}
""")

        create_file(base / "src/main.cpp", """
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "SampleController.h"

int main(int argc, char *argv[]) {
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    SampleController controller;
    engine.rootContext()->setContextProperty("controller", &controller);

    const QUrl url(QStringLiteral("views/main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
    }, Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}
""")

        create_file(base / "views/main.qml", f"""
import QtQuick
import QtQuick.Controls

ApplicationWindow {{
    visible: true
    width: 600
    height: 450
    title: "Batcaverna - C++ Qt Quick App ({project_name})"

    background: Rectangle {{
        color: "#1e1e2e"
    }}

    Column {{
        anchors.centerIn: parent
        spacing: 20

        Text {{
            text: "Bem-vindo ao C++ Qt Quick (QML)!"
            font.pixelSize: 24
            font.bold: true
            color: "#cdd6f4"
            anchors.horizontalCenter: parent.horizontalCenter
        }}

        Text {{
            text: "Nome atual no Controller: " + controller.name
            font.pixelSize: 16
            color: "#a6adc8"
            anchors.horizontalCenter: parent.horizontalCenter
        }}

        TextField {{
            id: nameInput
            placeholderText: "Digite seu nome..."
            color: "#cdd6f4"
            anchors.horizontalCenter: parent.horizontalCenter
            background: Rectangle {{
                implicitWidth: 200
                implicitHeight: 40
                color: "#313244"
                radius: 6
            }}
        }}

        Button {{
            text: "Enviar para C++"
            anchors.horizontalCenter: parent.horizontalCenter
            contentItem: Text {{
                text: parent.text
                color: "#11111b"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
            }}
            background: Rectangle {{
                implicitWidth: 150
                implicitHeight: 40
                color: parent.down ? "#a6e3a1" : "#89b4fa"
                radius: 8
            }}
            onClicked: {{
                controller.greet(nameInput.text)
            }}
        }}
    }}
}}
""")

        print(f"✅ Projeto C++ Qt Quick (QML) gerado com sucesso em {project_name}")
        print("👉 Para compilar e rodar:")
        print(f"   cd {project_name} && mkdir -p build && cd build")
        print("   cmake .. && make && ./cpp_qml_app")

    elif template_type == 5:
        # ==========================================
        # 5. C++ Qt Widgets (.ui + CMake)
        # ==========================================
        for folder in ["src", "views"]:
            (base / folder).mkdir(parents=True, exist_ok=True)

        create_file(base / "CMakeLists.txt", f"""
cmake_minimum_required(VERSION 3.16)
project(cpp_widgets_app VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOUIC_SEARCH_PATHS ${{CMAKE_CURRENT_SOURCE_DIR}}/views)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

add_executable(cpp_widgets_app
    src/main.cpp
    src/mainwindow.h
    src/mainwindow.cpp
    views/mainwindow.ui
)

target_link_libraries(cpp_widgets_app PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
)
""")

        create_file(base / "src/mainwindow.h", """
#pragma once
#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_btn_click_clicked();

private:
    Ui::MainWindow *ui;
};
""")

        create_file(base / "src/mainwindow.cpp", """
#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);
}

MainWindow::~MainWindow() {
    delete ui;
}

void MainWindow::on_btn_click_clicked() {
    QString text = ui->txt_input->text();
    if (!text.isEmpty()) {
        ui->lbl_title->setText("Texto do C++: " + text);
    } else {
        ui->lbl_title->setText("Digite algo em C++!");
    }
}
""")

        create_file(base / "src/main.cpp", """
#include <QApplication>
#include "mainwindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    MainWindow w;
    w.show();
    return app.exec();
}
""")

        create_file(base / "views/mainwindow.ui", """
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>500</width>
    <height>350</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Batcaverna - C++ Qt Widgets</string>
  </property>
  <property name="styleSheet">
   <string notr="true">QMainWindow { background-color: #1e1e2e; } QLabel { color: #cdd6f4; font-size: 16px; } QPushButton { background-color: #89b4fa; color: #11111b; border-radius: 6px; padding: 8px 16px; font-weight: bold; } QPushButton:hover { background-color: #b4befe; } QLineEdit { background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; border-radius: 6px; padding: 8px; }</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLabel" name="lbl_title">
      <property name="text">
       <string>C++ Widgets com arquivo .ui compilado!</string>
      </property>
      <property name="alignment">
       <set>Qt::AlignCenter</set>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLineEdit" name="txt_input">
      <property name="placeholderText">
       <string>Escreva em C++...</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="btn_click">
      <property name="text">
       <string>Executar em C++</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
""")

        print(f"✅ Projeto C++ Qt Widgets (.ui) gerado com sucesso em {project_name}")
        print("👉 Para compilar e rodar:")
        print(f"   cd {project_name} && mkdir -p build && cd build")
        print("   cmake .. && make && ./cpp_widgets_app")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python generator.py <project_name> <template_type>")
        sys.exit(1)
    
    p_name = sys.argv[1]
    try:
        t_type = int(sys.argv[2])
    except ValueError:
        print("O tipo de template deve ser um inteiro (1-5)")
        sys.exit(1)

    generate_project(p_name, t_type)
