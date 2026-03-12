import sys
from PySide6.QtWidgets import QApplication
from core.router import Router
from core.logger import get_logger
def main():
    app = QApplication(sys.argv)
    router = Router()
    router.navigate("/")
    router.show()
    get_logger("App").info("Projeto Elite Iniciado")
    sys.exit(app.exec())
if __name__ == "__main__": main()