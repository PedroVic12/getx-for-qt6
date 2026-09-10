from PySide6.QtCore import QObject, Slot, Signal, Property
from controllers.polyglot_controller import PolyglotController
from controllers.cv_controller import CurriculoController
from models.routine_model import RoutineModel

class AppController(QObject):
    """Controller Principal (MVC Central Coordinator) exposto ao QML."""

    toastMessage = Signal(str, str) # mensagem, tipo ('info', 'success', 'error')
    routineUpdated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.polyglot = PolyglotController(self)
        self.cv = CurriculoController(self)
        self.routine = RoutineModel()

        # Conecta sinais internos aos toasts da interface
        self.polyglot.outputEmitted.connect(lambda msg: self.toastMessage.emit(msg, "info"))
        self.cv.statusChanged.connect(lambda msg, ok: self.toastMessage.emit(msg, "success" if ok else "error"))

    @Slot(str, str, str)
    def run_polyglot_terminal(self, lang: str, file: str, params: str):
        self.polyglot.executar_no_terminal(lang, file, params)

    @Slot(str, str, str, result=str)
    def run_polyglot_inline(self, lang: str, file: str, params: str) -> str:
        return self.polyglot.executar_inline(lang, file, params)

    @Slot(str, str, str, result=bool)
    def generate_cv_pdf(self, vaga: str, objetivo: str, custom_path: str) -> bool:
        return self.cv.gerar_pdf(vaga, objetivo, custom_path)

    @Slot(str, str, str, result=bool)
    def generate_cv_docx(self, vaga: str, objetivo: str, custom_path: str) -> bool:
        return self.cv.gerar_docx(vaga, objetivo, custom_path)

    @Slot(int, result=bool)
    def toggle_postit_item(self, index: int) -> bool:
        res = self.routine.toggle_item(index)
        self.routineUpdated.emit()
        if self.routine.is_expediente_finalizado():
            self.toastMessage.emit("🎉 EXPEDIENTE FINALIZADO! 3 itens concluídos no Post-it!", "success")
        return res

    @Slot(result=int)
    def add_pomodoro(self) -> int:
        count = self.routine.add_pomodoro()
        self.routineUpdated.emit()
        self.toastMessage.emit(f"⏱️ Pomodoro adicionado! Total hoje: {count}", "info")
        return count

    @Slot(result=list)
    def get_postit_items(self) -> list:
        return self.routine.data["post_its"]

    @Slot(result=int)
    def get_pomodoros_count(self) -> int:
        return self.routine.data["pomodoros_hoje"]
