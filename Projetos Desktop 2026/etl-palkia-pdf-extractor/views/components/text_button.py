from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
class TextButton(QPushButton):
    def __init__(self, text, on_click=None, parent=None):
        super().__init__(text, parent)
        self.setObjectName("TextButton"); self.setCursor(Qt.PointingHandCursor)
        if on_click: self.clicked.connect(on_click)