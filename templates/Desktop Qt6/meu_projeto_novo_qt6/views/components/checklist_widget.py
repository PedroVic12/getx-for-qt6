from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QFrame
from PySide6.QtCore import Qt
class ChecklistWidget(QFrame):
    def __init__(self, markdown_text="", parent=None, on_toggle=None):
        super().__init__(parent); self.on_toggle = on_toggle; self.main_layout = QVBoxLayout(self); self.main_layout.setSpacing(15); self.main_layout.setContentsMargins(15, 15, 15, 15); self.render_markdown(markdown_text)
    def render_markdown(self, text):
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            if item.widget(): item.widget().setParent(None)
        lines = text.strip().split("\n")
        for line in lines:
            content = line.strip()
            if not content: continue
            if content.startswith("## "):
                header = QLabel(content.replace("## ", "")); header.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px;"); self.main_layout.addWidget(header)
            elif content.startswith("- ["):
                checkbox = QCheckBox(content[5:].strip()); checkbox.setChecked("[x]" in content.lower())
                checkbox.stateChanged.connect(lambda state, t=checkbox.text(): self.on_toggle(t, state == 2) if self.on_toggle else None)
                if line.startswith("  "): checkbox.setStyleSheet("margin-left: 35px;")
                self.main_layout.addWidget(checkbox)