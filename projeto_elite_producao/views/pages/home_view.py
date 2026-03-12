import os, sys, subprocess
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea
from core.base_view import StatefulView
from views.components.text_button import TextButton
from views.components.checklist_widget import ChecklistWidget
from controllers.home_controller import HomeController
class HomeView(StatefulView):
    def build(self):
        self.controller = HomeController()
        banner = QFrame(); banner.setStyleSheet("background: #E3F2FD; border: 1px solid #2196F3; border-radius: 5px;")
        layout = QVBoxLayout(banner); layout.addWidget(QLabel("🚀 <b>Pronto para começar?</b>"))
        btn = TextButton("@getx-for-qt6/gemini/** (Abrir Guia)", on_click=self.open_docs)
        layout.addWidget(btn); self.main_layout.addWidget(banner)
        self.main_layout.addWidget(QLabel("<h1>🏠 Dashboard</h1>"))
        md = self.controller.load_tasks_from_db()
        self.checklist = ChecklistWidget(md, on_toggle=self.controller.update_task_status)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(self.checklist)
        self.main_layout.addWidget(scroll)
    def open_docs(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "..", "gemini"))
        if sys.platform == 'win32': os.startfile(path)
        else: subprocess.Popen(['xdg-open', path])