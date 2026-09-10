import os
from PySide6.QtCore import QObject, Slot, Signal
from models.cv_model import CurriculoModel

class CurriculoController(QObject):
    """Controller do Gerador de Currículos KDE para QML."""

    statusChanged = Signal(str, bool) # mensagem, sucesso

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = CurriculoModel()

    @Slot(str, str, str, result=bool)
    def gerar_pdf(self, vaga: str, objetivo: str, custom_path: str) -> bool:
        if not custom_path:
            user_home = os.path.expanduser("~")
            custom_path = os.path.join(user_home, "Curriculo_Pedro_Veras.pdf")

        ok, msg = self.model.gerar_pdf(vaga.strip(), objetivo.strip(), custom_path)
        self.statusChanged.emit(msg, ok)
        return ok

    @Slot(str, str, str, result=bool)
    def gerar_docx(self, vaga: str, objetivo: str, custom_path: str) -> bool:
        if not custom_path:
            user_home = os.path.expanduser("~")
            custom_path = os.path.join(user_home, "Curriculo_Pedro_Veras.docx")

        ok, msg = self.model.gerar_docx(vaga.strip(), objetivo.strip(), custom_path)
        self.statusChanged.emit(msg, ok)
        return ok

    @Slot(result=str)
    def get_resumo_padrao(self) -> str:
        return self.model.dados["resumo"]
