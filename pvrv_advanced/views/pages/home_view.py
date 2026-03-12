from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QListWidget, QFrame
)
from PySide6.QtCore import Qt
from core.base_view import StatefulView
from controllers.home_controller import HomeController
from core.i18n import I18n

class HomeView(StatefulView):
    def __init__(self, router=None):
        # Primeiro definimos o controller
        controller = HomeController()
        # Chamamos o super
        super().__init__(router=router, controller=controller)

    def build(self):
        """Método chamado pelo super().__init__()"""
        # Garante que o estado tenha valores iniciais se ainda não tiverem sido setados
        if not self.state:
            self.state = {
                "greeting": "Olá! Como você se chama?",
                "tasks": self.controller.get_initial_tasks() if self.controller else []
            }

        # 1. Header do Dashboard
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        self.welcome_label = QLabel(I18n.t("home.welcome"))
        self.welcome_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        header_layout.addWidget(self.welcome_label)
        self.main_layout.addWidget(header_frame)

        # 2. Seção de Interação (Input + Botão)
        interaction_group = QFrame()
        interaction_group.setStyleSheet("background-color: #f9f9f9; border-radius: 10px; padding: 10px;")
        interaction_layout = QVBoxLayout(interaction_group)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite seu nome aqui...")
        self.name_input.setStyleSheet("padding: 10px; font-size: 16px; border: 1px solid #ccc;")
        interaction_layout.addWidget(self.name_input)

        self.btn_greet = QPushButton("Me cumprimentar! 🚀")
        self.btn_greet.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold; border: none;")
        self.btn_greet.clicked.connect(self.on_greet_click)
        interaction_layout.addWidget(self.btn_greet)

        # 3. Label de Resposta (Atualizado via State)
        self.greeting_display = QLabel(self.state["greeting"])
        self.greeting_display.setStyleSheet("font-size: 18px; color: #444; margin-top: 10px;")
        interaction_layout.addWidget(self.greeting_display)
        
        self.main_layout.addWidget(interaction_group)

        # 4. Seção de Lista de Tarefas (Dashboard-like)
        task_label = QLabel("📋 Minhas Tarefas do Dia:")
        task_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px;")
        self.main_layout.addWidget(task_label)

        self.task_list_widget = QListWidget()
        self.task_list_widget.setStyleSheet("border: 1px solid #eee; background-color: white; padding: 5px;")
        for task in self.state["tasks"]:
            self.task_list_widget.addItem(task)
        
        self.main_layout.addWidget(self.task_list_widget)
        self.main_layout.addStretch(1) # Empurra tudo para cima

    def on_greet_click(self):
        """Handler do clique que altera o estado da View"""
        name = self.name_input.text()
        message = self.controller.get_welcome_message(name)
        # Atualizamos o estado (Estilo Flutter setState)
        self.set_state(greeting=message)

    def update_ui(self):
        """Método chamado automaticamente sempre que o estado muda"""
        if hasattr(self, 'greeting_display'):
            self.greeting_display.setText(self.state.get("greeting", ""))
