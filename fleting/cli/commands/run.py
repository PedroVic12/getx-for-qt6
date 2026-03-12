import subprocess
import sys
import shutil
from pathlib import Path
from fleting.cli.console.console import console

def handle_run():
    project_root = Path.cwd()
    app_path = project_root / "main.py"

    if not app_path.exists():
        console.print("❌ main.py not found.", style="error")
        console.print("👉 Execute this command within a Fleting project.", style="suggestion")
        return

    # Tenta verificar se o PySide6 está instalado
    try:
        import PySide6
    except ImportError:
        console.print("❌ PySide6 is not installed in the environment.", style="error")
        console.print("👉 pip install PySide6", style="suggestion")
        return

    console.print("🚀 Starting Qt6 MVC application..\n", style="info")

    try:
        # Usa sys.executable para garantir que usamos o mesmo interpretador/venv
        subprocess.run(
            [sys.executable, str(app_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        console.print("❌ Error running the Qt application.", style="error")
