from PySide6.QtWidgets import QWidget, QVBoxLayout
class StatelessView(QWidget):
    def __init__(self, router=None, controller=None):
        super().__init__()
        self.router, self.controller, self.main_layout = router, controller, QVBoxLayout(self)
        self.build()
    def build(self): pass
class StatefulView(QWidget):
    def __init__(self, router=None, controller=None):
        super().__init__()
        self.router, self.controller, self.state, self.main_layout = router, controller, {}, QVBoxLayout(self)
        self.build()
    def set_state(self, **s): self.state.update(s); self.update_ui()
    def build(self): pass
    def update_ui(self): pass
