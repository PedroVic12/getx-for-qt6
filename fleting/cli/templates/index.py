from pathlib import Path
import json
import base64

ICON = "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"

def init_project(project_root: Path, project_name: str = "Qt6App"):
    """
    Initializes a PySide6 MVC project.
    """
    BASE = project_root

    def create_file(path, content=""):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    # Estrutura de Pastas
    folders = [
        "assets",
        "core",
        "configs",
        "controllers",
        "models",
        "views/layouts",
        "views/pages",
        "views/components",
    ]

    for folder in folders:
        (BASE / folder).mkdir(parents=True, exist_ok=True)

    # 1. CORE: base_view.py
    create_file(BASE / "core/base_view.py", """from PySide6.QtWidgets import QWidget

class BaseView(QWidget):
    def __init__(self, controller=None, router=None):
        super().__init__()
        self.controller = controller
        self.router = router
""")

    # 2. CORE: router.py
    create_file(BASE / "core/router.py", """from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
import importlib

class Router(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt6 MVC Framework")
        self.resize(800, 600)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.pages = {}

    def navigate(self, route_path):
        from configs.routes import ROUTES
        
        if route_path in self.pages:
            self.stack.setCurrentWidget(self.pages[route_path])
            return

        # Lazy Loading
        for r in ROUTES:
            if r["path"] == route_path:
                module = importlib.import_module(r["module"])
                view_class = getattr(module, r["view_class"])
                view_instance = view_class(router=self)
                
                self.stack.addWidget(view_instance)
                self.pages[route_path] = view_instance
                self.stack.setCurrentWidget(view_instance)
                return
        
        print(f"Rota {route_path} não encontrada.")
""")

    # 3. CONFIGS: routes.py
    create_file(BASE / "configs/routes.py", """ROUTES = [
    {
        "path": "/",
        "view_class": "HomeView",
        "module": "views.pages.home_view",
        "label": "Home",
    },
]
""")

    # 4. VIEWS: pages/home_view.py
    create_file(BASE / "views/pages/home_view.py", """from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from controllers.home_controller import HomeController

class HomeView(QWidget):
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.controller = HomeController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Bem-vindo ao seu novo App Qt6 MVC!")
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(label)
        
        btn = QPushButton("Ir para Configurações (Exemplo)")
        layout.addWidget(btn)
""")

    # 5. CONTROLLERS: home_controller.py
    create_file(BASE / "controllers/home_controller.py", """from PySide6.QtCore import QObject

class HomeController(QObject):
    def __init__(self):
        super().__init__()

    def get_title(self):
        return "Home Page"
""")

    # 6. MODELS: home_model.py
    create_file(BASE / "models/home_model.py", """class HomeModel:
    def __init__(self):
        self.data = {}
""")

    # 7. main.py
    create_file(BASE / "main.py", """import sys
from PySide6.QtWidgets import QApplication
from core.router import Router

def main():
    app = QApplication(sys.argv)
    
    # Estilo Global (Opcional)
    # with open("assets/style.qss", "r") as f:
    #     app.setStyleSheet(f.read())
    
    router = Router()
    router.navigate("/")
    router.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
""")

    # 8. .fleting flag
    (BASE / ".fleting").write_text("fleting-qt6-project", encoding="utf-8")