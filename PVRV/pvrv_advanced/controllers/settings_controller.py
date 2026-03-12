from PySide6.QtCore import QObject

class SettingsController(QObject):
    def __init__(self):
        super().__init__()

    def get_title(self):
        return "Settings Page"
