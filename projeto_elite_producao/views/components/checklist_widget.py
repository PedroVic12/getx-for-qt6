from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QFrame
class ChecklistWidget(QFrame):
    def __init__(self, md="", parent=None, on_toggle=None):
        super().__init__(parent); self.on_toggle = on_toggle; self.main_layout = QVBoxLayout(self)
        self.render_markdown(md)
    def render_markdown(self, text):
        for i in reversed(range(self.main_layout.count())):
            if self.main_layout.itemAt(i).widget(): self.main_layout.itemAt(i).widget().setParent(None)
        for line in text.strip().split("\n"):
            c = line.strip()
            if not c: continue
            if c.startswith("## "):
                l = QLabel(c.replace("## ", "")); l.setStyleSheet("font-size: 20px; font-weight: bold;"); self.main_layout.addWidget(l)
            elif c.startswith("- ["):
                cb = QCheckBox(c[5:].strip()); cb.setChecked("[x]" in c.lower())
                cb.stateChanged.connect(lambda s, t=cb.text(): self.on_toggle(t, s == 2) if self.on_toggle else None)
                self.main_layout.addWidget(cb)