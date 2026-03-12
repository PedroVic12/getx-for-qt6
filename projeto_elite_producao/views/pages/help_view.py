from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class HelpView(StatelessView):
    def build(self): self.main_layout.addWidget(QLabel('📚 Central de Ajuda'))