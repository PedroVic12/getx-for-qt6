# 🗄️ Guia de Banco de Dados, Migrations e CRUD

Este guia explica como gerenciar dados no seu framework PySide6 MVC usando SQLite3.

## 🚀 1. Migrations Simples com SQLite
Como não usamos um ORM pesado (como SQLAlchemy), as migrations são feitas via scripts SQL em `migrations/`.

### Fluxo Recomendado:
1. Crie um arquivo `.sql` em `migrations/` (ex: `002_add_description_to_tasks.sql`).
2. Crie um script `db_migrate.py` na raiz (ou use o `fleting db migrate` se configurado) que lê esses arquivos e executa o SQL.

## 📊 2. Modelagem de Dados (Entity Pattern)
Para manter o código limpo, use `dataclasses` para representar seus dados no Python.

```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    completed: bool
```

## 🛠️ 3. Checklist para Projetos CRUD
Sempre que for criar um novo módulo de CRUD (ex: Clientes, Produtos), siga este checklist:

- [ ] **Database**: Criar a tabela no SQLite (`CREATE TABLE...`).
- [ ] **Model**: Criar a classe de dados em `models/nome_model.py`.
- [ ] **Controller**: Implementar 4 métodos fundamentais:
    - `create(data)`
    - `get_all()`
    - `update(id, data)`
    - `delete(id)`
- [ ] **View (Stateful)**: 
    - `build()`: Criar formulário e lista.
    - `update_ui()`: Atualizar a lista após salvar ou deletar.
- [ ] **Router**: Registrar a nova rota em `configs/routes.py`.

## 💡 Dica de Ouro: Persistência Atômica
No Qt, prefira salvar no banco de dados no evento `stateChanged` do componente (como fizemos no Checklist), isso evita a necessidade de um botão "Salvar" e torna o App muito mais moderno (estilo Notion/Google Keep).
