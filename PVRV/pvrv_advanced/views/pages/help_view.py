from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from controllers.help_controller import HelpController

class HelpView(QWidget):
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.controller = HelpController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Visualizando Página: Help")
        label.setStyleSheet("font-size: 24px;")
        layout.addWidget(label)
