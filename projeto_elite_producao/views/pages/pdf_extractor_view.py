from PySide6.QtWidgets import QLabel
from core.base_view import StatelessView
class Pdf_extractorView(StatelessView):
    def build(self): self.main_layout.addWidget(QLabel('📄 PDF Extractor'))