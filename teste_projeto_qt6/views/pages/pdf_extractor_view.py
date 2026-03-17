from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class Pdf_extractorView(StatelessView):
    def build(self):
        label = QLabel("📄 Extrator de PDF Palkia. ETL de PDFs integrada."); label.setStyleSheet("font-size: 20px;"); self.main_layout.addWidget(label)
