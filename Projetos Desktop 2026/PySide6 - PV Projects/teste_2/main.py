import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Property, Signal

class MainController(QObject):
    nameChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self._name = "Pedro"

    @Property(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._name != value:
            self._name = value
            self.nameChanged.emit(value)

    @Slot(str)
    def greet(self, user_name):
        print(f"Olá do Python para {user_name}!")
        self.name = user_name

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    controller = MainController()
    engine.rootContext().setContextProperty("controller", controller)

    qml_file = os.path.join(os.path.dirname(__file__), 'views', 'main.qml')
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    print("Aplicação Qt Quick iniciada com sucesso!")
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
