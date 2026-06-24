from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class Teste_1View(StatelessView):
    def build(self):
        label = QLabel("📄 View Principal do projeto: teste_1"); label.setStyleSheet("font-size: 20px;"); self.main_layout.addWidget(label)
