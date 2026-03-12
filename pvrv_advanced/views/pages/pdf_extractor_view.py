from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from controllers.pdf_extractor_controller import Pdf_extractorController

class Pdf_extractorView(QWidget):
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.controller = Pdf_extractorController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Visualizando Página: Pdf_extractor")
        label.setStyleSheet("font-size: 24px;")
        layout.addWidget(label)
