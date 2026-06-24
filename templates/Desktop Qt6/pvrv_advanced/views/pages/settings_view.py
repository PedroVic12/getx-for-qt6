from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView

class SettingsView(StatelessView):
    def build(self):
        label = QLabel("⚙️ Configurações do Sistema. Ajuste as preferências do framework.")
        label.setStyleSheet("font-size: 20px;")
        self.main_layout.addWidget(label)
