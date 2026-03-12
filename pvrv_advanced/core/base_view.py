from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QObject, Signal

class StatelessView(QWidget):
    """
    Equivalente ao StatelessWidget do Flutter.
    O layout é fixo no init. Depende apenas das props passadas.
    """
    def __init__(self, router=None, controller=None):
        super().__init__()
        self.router = router
        self.controller = controller
        self.main_layout = QVBoxLayout(self)
        self.build()

    def build(self):
        # Sobrescrever na subclasse para definir o layout inicial
        pass

class StatefulView(QWidget):
    """
    Equivalente ao StatefulWidget do Flutter.
    Possui um método set_state() que pode ser usado para atualizar partes da UI.
    """
    def __init__(self, router=None, controller=None):
        super().__init__()
        self.router = router
        self.controller = controller
        self.state = {}
        self.main_layout = QVBoxLayout(self)
        self.build()

    def set_state(self, **new_state):
        self.state.update(new_state)
        self.update_ui()

    def build(self):
        # Sobrescrever na subclasse para definir o layout inicial
        pass

    def update_ui(self):
        # Sobrescrever na subclasse para atualizar widgets baseados no state
        pass
