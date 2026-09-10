import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from backend import ProcessManager

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Registra o backend para o QML
    backend = ProcessManager()
    engine.rootContext().setContextProperty("backend", backend)

    # Carrega a interface
    qml_file = os.path.join(os.path.dirname(__file__), "ui", "main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
