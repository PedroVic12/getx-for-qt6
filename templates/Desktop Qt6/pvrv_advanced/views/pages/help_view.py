from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView

class HelpView(StatelessView):
    def build(self):
        label = QLabel("📚 Central de Ajuda. Aqui você encontra os guias de uso.")
        label.setStyleSheet("font-size: 20px;")
        self.main_layout.addWidget(label)
