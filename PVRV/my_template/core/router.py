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
