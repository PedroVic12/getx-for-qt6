import sqlite3
from pathlib import Path

def get_connection():
    # Caminho do banco dentro da pasta data do projeto
    db_path = Path("data/app.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn
