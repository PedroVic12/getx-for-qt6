# 🧩 Componentes Reutilizáveis (Templates para a CLI)

Este guia contém as especificações de componentes customizados que a CLI deve ser capaz de gerar no PySide6/Qt6, integrados ao MVC.

## 1. Page (View Completa)
Gera uma página com layout pronto para ser populada.

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class HomeView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Página Inicial")
        self.layout.addWidget(self.label)
```

## 2. Controller (MVC Logic)
Gera um controlador com suporte a Signals e Threading (como no Palkia).

```python
from PySide6.QtCore import QObject, Signal

class HomeController(QObject):
    # Signals para atualizar a View
    status_changed = Signal(str)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def handle_button_click(self):
        # Lógica aqui (pode chamar o model ou disparar uma thread)
        self.status_changed.emit("Iniciando tarefa...")
```

## 3. Worker (Threading Template)
Componente gerado para processamento pesado em background.

```python
from PySide6.QtCore import QObject, Signal, QRunnable

class TaskWorker(QObject):
    finished = Signal()
    progress = Signal(int)
    error = Signal(str)

    def run(self):
        try:
            # Processamento pesado aqui (ex: Pandas, PDF Extraction)
            self.progress.emit(100)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
```

## 4. Loading Overlay (UI Component)
Componente de UI que cobre a tela durante tarefas demoradas.

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.loading_label = QLabel("Carregando...")
        layout.addWidget(self.loading_label)
```

## 5. Notification Manager (UI Component)
Sistema de toast notifications flutuantes.

```python
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import QTimer, Qt

class NotificationManager(QWidget):
    def show_message(self, message):
        # Mostrar toast com animação de fade (inspirado no Palkia)
        pass
```
