from PySide6.QtCore import QObject

class Pdf_extractorController(QObject):
    def __init__(self):
        super().__init__()

    def get_title(self):
        return "Pdf_extractor Page"
