from PySide6.QtCore import QObject

class HelpController(QObject):
    def __init__(self):
        super().__init__()

    def get_title(self):
        return "Help Page"
