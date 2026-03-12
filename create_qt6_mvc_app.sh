#!/bin/bash

#!/bin/bash

# Se o primeiro argumento ($1) estiver vazio, pede o input do usuário
if [ -z "$1" ]; then
    read -p "📂 Digite o nome do projeto: " PROJECT_NAME
else
    PROJECT_NAME=$1
fi

# Define um valor padrão caso o usuário apenas dê 'Enter' no input
PROJECT_NAME=${PROJECT_NAME:-"qt6_app"}

echo "🚀 Iniciando framework PySide6 MVC em: $PROJECT_NAME"


mkdir -p $PROJECT_NAME/{assets,core,configs/languages,controllers,models,views/pages,views/layouts,views/components}

# 1. CORE: logger.py (Adaptado)
cat <<EOF > $PROJECT_NAME/core/logger.py
import logging
from pathlib import Path

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    return logger
EOF

# 2. CORE: i18n.py
cat <<EOF > $PROJECT_NAME/core/i18n.py
import json
from pathlib import Path

class I18n:
    translations = {}
    language = "pt"

    @classmethod
    def load(cls, lang):
        cls.language = lang
        path = Path("configs/languages") / f"{lang}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                cls.translations = json.load(f)

    @classmethod
    def t(cls, key):
        value = cls.translations
        for k in key.split("."):
            value = value.get(k, key)
            if value == key: break
        return value
EOF

# 3. CORE: router.py (O motor de navegação Qt6)
cat <<EOF > $PROJECT_NAME/core/router.py
from PySide6.QtWidgets import QMainWindow, QStackedWidget
import importlib
from core.logger import get_logger

logger = get_logger("Router")

class Router(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.pages = {}
        self.setWindowTitle("Qt6 MVC Framework")

    def navigate(self, route_path):
        from configs.routes import ROUTES
        
        if route_path in self.pages:
            self.stack.setCurrentWidget(self.pages[route_path])
            logger.info(f"Navegando para cache: {route_path}")
            return

        for r in ROUTES:
            if r["path"] == route_path:
                module = importlib.import_module(r["module"])
                view_class = getattr(module, r["view_class"])
                view_instance = view_class(router=self)
                
                self.stack.addWidget(view_instance)
                self.pages[route_path] = view_instance
                self.stack.setCurrentWidget(view_instance)
                logger.info(f"Navegando para nova view: {route_path}")
                return
        
        logger.warning(f"Rota {route_path} não encontrada.")
EOF

# 4. CONFIGS: app_config.py
cat <<EOF > $PROJECT_NAME/configs/app_config.py
class AppConfig:
    APP_NAME = "$PROJECT_NAME"
    DEFAULT_SCREEN = {"width": 1280, "height": 800}
EOF

# 5. CONFIGS: routes.py
cat <<EOF > $PROJECT_NAME/configs/routes.py
ROUTES = [
    {
        "path": "/",
        "view_class": "HomeView",
        "module": "views.pages.home_view",
        "label": "Home",
    },
]
EOF

# 6. Languages (JSON)
cat <<EOF > $PROJECT_NAME/configs/languages/pt.json
{
  "app": { "name": "$PROJECT_NAME" },
  "home": { "welcome": "Bem-vindo ao framework Qt6 MVC" }
}
EOF

# 7. main.py (ESPELHO DO SEU PVRV/main.py)
cat <<EOF > $PROJECT_NAME/main.py
import sys
from PySide6.QtWidgets import QApplication
from configs.app_config import AppConfig
from core.logger import get_logger
import runtime_imports 

logger = get_logger("App")

def main():
    app = QApplication(sys.argv)
    
    try:
        # No PySide6, o assets_dir é gerenciado pelo QDir ou caminhos relativos
        
        from core.i18n import I18n
        I18n.load("pt")

        from core.router import Router
        router = Router()
        
        # Ajusta tamanho da janela conforme AppConfig
        router.resize(AppConfig.DEFAULT_SCREEN["width"], AppConfig.DEFAULT_SCREEN["height"])
        
        router.navigate("/")
        router.show()

        logger.info("Aplicação iniciada com sucesso")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Erro Crítico: {e}")

if __name__ == "__main__":
    main()
EOF

# 8. runtime_imports.py
touch $PROJECT_NAME/runtime_imports.py

# 9. Home View e Controller de Exemplo
cat <<EOF > $PROJECT_NAME/controllers/home_controller.py
class HomeController:
    def get_title(self):
        return "Página Inicial MVC"
EOF

cat <<EOF > $PROJECT_NAME/views/pages/home_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from controllers.home_controller import HomeController
from core.i18n import I18n

class HomeView(QWidget):
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.controller = HomeController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel(I18n.t("home.welcome"))
        title.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(title)
        layout.addWidget(QLabel(self.controller.get_title()))
EOF

echo "✅ Framework gerado com sucesso em $PROJECT_NAME"
echo "👉 Para rodar: cd $PROJECT_NAME && python3 main.py"
