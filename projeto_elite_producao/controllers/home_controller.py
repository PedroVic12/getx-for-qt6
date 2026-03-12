from core.database import get_connection
class HomeController:
    def load_tasks_from_db(self):
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, completed INTEGER)")
        cursor.execute("SELECT title, completed FROM tasks")
        rows = cursor.fetchall()
        if not rows:
            tasks = ["Configurar Qt6", "Sidebar Responsiva", "Dark Mode Fix"]
            for t in tasks: cursor.execute("INSERT OR IGNORE INTO tasks (title, completed) VALUES (?, 0)", (t,))
            conn.commit(); cursor.execute("SELECT title, completed FROM tasks"); rows = cursor.fetchall()
        md = "## 📋 Tarefas Persistentes\n"
        for r in rows: md += f"- [{'x' if r['completed'] else ' '}] {r['title']}\n"
        return md
    def update_task_status(self, title, completed):
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE title = ?", (1 if completed else 0, title))
        conn.commit()