from PySide6.QtCore import QObject
from core.database import get_connection

class HomeController(QObject):
    def __init__(self):
        super().__init__()

    def get_welcome_message(self, name):
        if not name: return "Por favor, digite seu nome acima."
        return f"Olá, {name}. Prazer em conhecer você! 👋"

    def load_tasks_from_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, completed FROM tasks")
        rows = cursor.fetchall()
        
        # Se não houver nada, insere as iniciais
        if not rows:
            self.seed_initial_tasks()
            cursor.execute("SELECT title, completed FROM tasks")
            rows = cursor.fetchall()
        
        # Converte para Markdown format
        md = "## 📋 Minhas Tarefas (DB Persistente)\n"
        for row in rows:
            status = "x" if row["completed"] == 1 else " "
            md += f"- [{status}] {row['title']}\n"
        return md

    def update_task_status(self, title, completed):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE title = ?", (1 if completed else 0, title))
        conn.commit()

    def seed_initial_tasks(self):
        tasks = [
            "Configurar PySide6 MVC",
            "Criar Sidebar Responsiva",
            "Implementar Loader Palkia",
            "Finalizar Dark Mode Fix"
        ]
        conn = get_connection()
        cursor = conn.cursor()
        for t in tasks:
            cursor.execute("INSERT OR IGNORE INTO tasks (title, completed) VALUES (?, 0)", (t,))
        conn.commit()
