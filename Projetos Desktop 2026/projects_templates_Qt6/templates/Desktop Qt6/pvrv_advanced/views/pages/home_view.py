import os, sys, subprocess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QScrollArea, QFrame
)
from core.base_view import StatefulView
from controllers.home_controller import HomeController
from views.components.checklist_widget import ChecklistWidget
from views.components.text_button import TextButton
from core.i18n import I18n

class HomeView(StatefulView):
    def __init__(self, router=None):
        super().__init__(router=router, controller=HomeController())

    def build(self):
        # 1. Recomendação de Documentação (LINK ANCORA)
        doc_frame = QFrame()
        doc_frame.setStyleSheet("background-color: #E3F2FD; border-radius: 5px; border: 1px solid #2196F3;")
        doc_layout = QVBoxLayout(doc_frame)
        doc_msg = QLabel("💡 <b>Dica de Elite:</b> Leia a documentação técnica para começar:")
        doc_msg.setStyleSheet("color: #0D47A1;")
        doc_layout.addWidget(doc_msg)
        
        # Este botão agora abre o explorador de arquivos!
        self.btn_gemini = TextButton("@getx-for-qt6/gemini/** (Abrir Guia no Explorador)", 
                                     on_click=self.open_gemini_docs)
        doc_layout.addWidget(self.btn_gemini)
        self.main_layout.addWidget(doc_frame)

        # 2. Header
        self.welcome_label = QLabel(I18n.t("home.welcome"))
        self.welcome_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-top: 10px;")
        self.main_layout.addWidget(self.welcome_label)

        # 3. Input Nome
        interaction_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Seu nome...")
        interaction_layout.addWidget(self.name_input, 3)
        self.btn_greet = QPushButton("🚀")
        self.btn_greet.setFixedSize(50, 50)
        self.btn_greet.clicked.connect(self.on_greet_click)
        interaction_layout.addWidget(self.btn_greet)
        self.main_layout.addLayout(interaction_layout)

        self.greeting_display = QLabel("Olá!")
        self.main_layout.addWidget(self.greeting_display)

        # 4. Checklist Persistente
        md_content = self.controller.load_tasks_from_db()
        self.checklist = ChecklistWidget(md_content, on_toggle=self.on_task_toggled)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.checklist)
        self.main_layout.addWidget(scroll)

    def open_gemini_docs(self):
        """Abre o explorador de arquivos na pasta de documentação"""
        # Caminho absoluto da pasta gemini
        path = "/home/pedrov12/Documentos/GitHub/getx-for-qt6/gemini"
        
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            # Linux (seu sistema)
            subprocess.Popen(['xdg-open', path])
        print(f"Abrindo explorador em: {path}")

    def on_task_toggled(self, title, completed):
        self.controller.update_task_status(title, completed)

    def on_greet_click(self):
        msg = self.controller.get_welcome_message(self.name_input.text())
        self.greeting_display.setText(msg)
