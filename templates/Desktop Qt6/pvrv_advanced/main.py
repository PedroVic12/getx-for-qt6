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
        
        # O tema agora é aplicado automaticamente no Router.apply_theme()
        router.navigate("/")
        router.show()

        logger.info("Aplicação Desktop PVRV iniciada com sucesso")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Erro Crítico no Boot: {e}")

if __name__ == "__main__":
    main()
