from PySide6.QtWidgets import QMainWindow, QStackedWidget
import importlib
from core.logger import get_logger

logger = get_logger("Router")

class Router(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PVRV Advanced Qt6 Dashboard")
        self.resize(1000, 800)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.pages = {}

    def navigate(self, route_path):
        from configs.routes import ROUTES
        
        if route_path in self.pages:
            self.stack.setCurrentWidget(self.pages[route_path])
            logger.info(f"Navegando (cache): {route_path}")
            return

        # Procura a rota no arquivo de configuração
        for r in ROUTES:
            if r["path"] == route_path:
                try:
                    module = importlib.import_module(r["module"])
                    view_class = getattr(module, r["view_class"])
                    # Instancia a View passando o router para navegação futura
                    view_instance = view_class(router=self)
                    
                    self.stack.addWidget(view_instance)
                    self.pages[route_path] = view_instance
                    self.stack.setCurrentWidget(view_instance)
                    logger.info(f"Navegando (nova view): {route_path}")
                    return
                except Exception as e:
                    logger.error(f"Erro ao carregar rota {route_path}: {e}")
                    return
        
        logger.warning(f"Rota {route_path} não encontrada no configs/routes.py")
