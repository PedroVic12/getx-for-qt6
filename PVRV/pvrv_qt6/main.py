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
