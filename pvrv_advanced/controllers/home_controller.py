from PySide6.QtCore import QObject

class HomeController(QObject):
    def __init__(self):
        super().__init__()

    def get_welcome_message(self, name):
        if not name:
            return "Por favor, digite seu nome acima."
        return f"Olá, {name}. Prazer em conhecer você! 👋"

    def get_initial_tasks(self):
        return [
            "Configurar ambiente Qt6",
            "Criar primeira View Stateful",
            "Integrar Controller com Signals",
            "Estilizar Dashboard com QSS"
        ]
