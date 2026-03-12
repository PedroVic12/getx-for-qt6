from pathlib import Path
from fleting.cli.console.console import console

def is_fleting_project(path: Path) -> bool:
    return (path / "main.py").exists() and (path / "views").exists()

def get_project_root() -> Path:
    return Path.cwd()

def handle_create(args):
    
    root = get_project_root()

    if not is_fleting_project(root):
        console.print("❌ This directory is not a Fleting project.", style="error")
        console.print("👉 Execute this command within the project folder.", style="suggestion")
        return
    
    if len(args) < 2:
        console.print("Use: fleting create <controller|view|model|page> <nome>", style="suggestion")
        return

    kind, name = args[0], args[1]
    name = name.lower()

    try:
        if kind == "controller":
            create_controller(name)
        elif kind == "view":
            create_view(name)
        elif kind == "model":
            create_model(name)
        elif kind == "page":
            create_page(name)
        else:
            console.print(f"Unsupported Type: {kind}", style="warning")

    except Exception as e:
        console.print(f"Error creating {kind} {name}: {e}", style="error")

# --------------
# create controller
# --------------
def to_pascal_case(text: str) -> str:
    return "".join(word.capitalize() for word in text.split("_"))

def create_controller(name: str):
    BASE = get_project_root()
    path = BASE / "controllers" / f"{name}_controller.py"

    if path.exists():
        console.print(f"Controller '{name}' already exists.", style="warning")
        return

    class_name = f"{to_pascal_case(name)}Controller"
    model_class = f"{to_pascal_case(name)}Model"

    content = f'''from PySide6.QtCore import QObject, Signal
from models.{name}_model import {model_class}

class {class_name}(QObject):
    """
    Controller for {name} page
    """
    # Exemplo de Signal para atualizar a View
    data_updated = Signal(object)

    def __init__(self, model=None):
        super().__init__()
        self.model = model or {model_class}

    def get_title(self):
        return "{to_pascal_case(name)}"
'''
    path.write_text(content, encoding="utf-8")
    console.print(f"Controller successfully created: {name}", style="success")

# --------------
# create view
# --------------
def create_view(name: str):
    BASE = get_project_root()
    path = BASE / "views" / "pages" / f"{name}_view.py"

    if path.exists():
        console.print(f"View '{name}' already exists.", style="warning")
        return

    class_name = f"{name.capitalize()}View"

    content = f"""from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class {class_name}(QWidget):
    def __init__(self, controller=None, router=None):
        super().__init__()
        self.controller = controller
        self.router = router
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.label = QLabel("{name.capitalize()} View")
        layout.addWidget(self.label)
"""

    path.write_text(content, encoding="utf-8")
    console.print(f"View successfully created: {name}", style="success")


# --------------
# create model
# --------------
def create_model(name: str):
    BASE = get_project_root()
    path = BASE / "models" / f"{name}_model.py"

    if path.exists():
        console.print(f"Model '{name}' already exists.", style="warning")
        return

    class_name = f"{name.capitalize()}Model"

    content = f"""from core.base_model import BaseModel

class {class_name}(BaseModel):
    table_name = "{name}"
"""

    path.write_text(content, encoding="utf-8")
    console.print(f"Model successfully created: {name}", style="success")

# --------------
# create page
# --------------
def create_page(name: str):
    console.print(f"Creating a complete page: {name}", style="info")
    try:
        create_model(name)
        create_controller(name)
        create_page_view(name)
        register_route(name)
    except Exception as e:
        console.print("Error creating page: ", str(e), style="error")

def register_route(name: str):
    BASE = get_project_root()
    routes_file = BASE / "configs" / "routes.py"

    if not routes_file.exists():
        console.print("❌ configs/routes.py not found", style="error")
        return

    route_block = f"""
    {{
        "path": "/{name}",
        "view_class": "{name.capitalize()}View",
        "module": "views.pages.{name}_view",
        "label": "{name.capitalize()}",
    }},
"""

    content = routes_file.read_text(encoding="utf-8")

    # evita duplicar
    if f'"path": "/{name}"' in content:
        console.print(f"⚠️ Route '/{name}' already exists.", style="warning")
        return

    if "ROUTES = [" not in content:
        console.print("❌ ROUTES structure not found", style="error")
        return

    content = content.replace(
        "ROUTES = [",
        "ROUTES = [" + route_block,
        1,
    )

    routes_file.write_text(content, encoding="utf-8")
    console.print(f"✅ Route '/{name}' successfully registered", style="success")

def create_page_view(name: str):
    BASE = get_project_root()
    path = BASE / "views" / "pages" / f"{name}_view.py"

    if path.exists():
        console.print(f"View '{name}' already exists.", style="warning")
        return

    class_name = f"{name.capitalize()}View"
    controller_class = f"{name.capitalize()}Controller"

    content = f"""from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from controllers.{name}_controller import {controller_class}

class {class_name}(QWidget):
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.controller = {controller_class}()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.title_label = QLabel(self.controller.get_title())
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Exemplo de interação
        self.btn = QPushButton("Clique aqui")
        self.btn.clicked.connect(lambda: print("Botão da página {name} clicado!"))
        self.layout.addWidget(self.btn)
"""
    path.write_text(content, encoding="utf-8")
    console.print(f"Page created successfully: {name}", style="success")
