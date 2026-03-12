from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from controllers.home_controller import HomeController
from core.i18n import I18n

class HomeView(QWidget):
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.controller = HomeController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel(I18n.t("home.welcome"))
        title.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(title)
        layout.addWidget(QLabel(self.controller.get_title()))
