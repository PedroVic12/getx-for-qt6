from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
class TextButton(QPushButton):
    def __init__(self, t, on_click=None, p=None):
        super().__init__(t, p); self.setObjectName('TextButton'); self.setCursor(Qt.PointingHandCursor)
        if on_click: self.clicked.connect(on_click)