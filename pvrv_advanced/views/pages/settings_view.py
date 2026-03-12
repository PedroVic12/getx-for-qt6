from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from controllers.settings_controller import SettingsController

class SettingsView(QWidget):
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.controller = SettingsController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Visualizando Página: Settings")
        label.setStyleSheet("font-size: 24px;")
        layout.addWidget(label)
