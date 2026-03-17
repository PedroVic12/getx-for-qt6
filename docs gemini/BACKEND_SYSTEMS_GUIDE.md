# 🌐 Backend, APIs e Persistência: Guia Multi-Stack

Este guia detalha como estruturar backends modernos, consumir dados no React e gerenciar o SQLite nativo no PySide6.

---

## 🏗️ 1. Paradigmas de Backend: POO vs Funcional

A escolha do paradigma depende da complexidade da regra de negócio.

### 🐍 Python (FastAPI / Flask)
- **Mindset POO**: Use **Service Layers**. Uma classe `UserService` gerencia a lógica, e o `Route` apenas chama o método.
- **Dica FastAPI**: Use `Pydantic` para validação automática. É o "TypeScript do Python".

### 🟢 Node.js (Express)
- **Mindset Funcional**: O Express é baseado em **Middlewares** (funções encadeadas).
- **Dica**: Mantenha as funções puras. O `req` e `res` passam por transformadores até chegar na resposta final.

### 🦀 Rust (Tauri V2 / CLI)
- **Mindset Híbrido**: Rust usa **Traits** (interfaces) e **Structs**. Não há herança de classe, mas há polimorfismo via Traits.
- **Tauri V2**: Use o sistema de `Commands`. O frontend chama uma função Rust diretamente como se fosse uma API local.

---

## ⚛️ 2. Dica Master: Consumindo no React via Fetch Natural

Evite bibliotecas pesadas se não precisar de cache complexo. Use o padrão de **API Service**:

```javascript
// services/api.js
const BASE_URL = "http://localhost:8000";

export const api = {
  get: async (endpoint) => {
    const res = await fetch(`${BASE_URL}${endpoint}`);
    if (!res.ok) throw new Error("Erro na rede");
    return res.json();
  },
  post: async (endpoint, data) => {
    return fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(r => r.json());
  }
};
```

---

## 🗄️ 3. SQLite3 Nativo no PySide6 (Mindset Elite)

No nosso framework, o SQLite3 é tratado como um cidadão de primeira classe.

### Por que `sqlite3.Row`?
No `core/database.py`, usamos `conn.row_factory = sqlite3.Row`. Isso permite que você acesse os dados assim:
`row["title"]` em vez de `row[1]`. Isso evita bugs se você mudar a ordem das colunas no banco.

### Dicas de Performance:
1. **Conexões Curtas**: Abra a conexão no Controller, faça a operação e feche (ou use um Context Manager).
2. **Write-Ahead Logging (WAL)**: Para apps desktop rápidos, execute `PRAGMA journal_mode=WAL;` ao iniciar o banco.

---

## 🚀 4. Mergulho nas Migrations

Nosso sistema de migrations (em `migrations/`) segue o padrão de **Versionamento Incremental**.

### Como Funciona:
1. **Ordem Numérica**: Arquivos como `001_create_users.sql`, `002_add_email.sql`. O sistema lê a pasta em ordem alfabética.
2. **Tabela de Controle**: O banco possui uma tabela interna `_migrations`. Se o arquivo `001` já está lá, o sistema pula para o próximo.
3. **Idempotência**: Sempre que possível, use `CREATE TABLE IF NOT EXISTS`. Isso garante que o app não quebre se for reiniciado durante uma atualização.

### Checklist de Nova Migration:
- [ ] Criar arquivo `.sql` ou `.py` em `migrations/`.
- [ ] Testar o SQL no seu editor favorito (DBeaver/SQLite Browser).
- [ ] Rodar o App (O `init_project` já deve disparar a migração no boot).

---

## 💡 Conclusão: O Elo de Ligação
Seja em **Node**, **Python** ou **Rust**, o segredo é a **Contratação de Interface**. Se o seu Backend entrega um JSON limpo, o seu Frontend (React ou PySide6) não precisa saber qual linguagem o gerou. 

**Isso é desacoplamento de verdade.**
