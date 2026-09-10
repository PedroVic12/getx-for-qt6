import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from app import PolyglotBackend

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Registra o backend Python/C++/Julia/Lua no QML
    backend = PolyglotBackend()
    engine.rootContext().setContextProperty("backend", backend)
    
    qml_file = os.path.join(os.path.dirname(__file__), "ui", "main.qml")
    engine.load(qml_file)
    
    if not engine.rootObjects():
        sys.exit(-1)
        
    sys.exit(app.exec())
