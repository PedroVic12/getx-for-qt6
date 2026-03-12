# 🛠️ Guia do CLI — Qt6 Edition (Inspirado no Fleting)

Este guia descreve como os comandos da CLI devem funcionar após a migração para PySide6/Qt6.

## 🚀 Inicialização de Projeto

```bash
fleting init <nome_projeto>
cd <nome_projeto>
fleting run
```

### O que o `init` gera para Qt6:
- Estrutura de pastas `controllers/`, `models/`, `views/`, `core/`.
- `main.py` com o loop do `QApplication`.
- `core/router.py` com um `QMainWindow` e `QStackedWidget`.
- `assets/style.qss` (Arquivo CSS padrão para Qt).

---

## 🖥️ Comandos de Criação

### `fleting create page <nome>`
Cria o trio MVC (Model + Controller + View) para uma tela completa.

**Diferencial Qt6:**
- A **View** gerada herda de `QWidget` e define layouts do Qt.
- O **Controller** gerado contém handlers para eventos da View.
- O arquivo `configs/routes.py` (ou `core/router.py`) é atualizado com o import da nova página.

### `fleting create component <nome>`
Cria um widget customizado reutilizável em `views/components/`.

**Diferencial Qt6:**
- Gera uma classe simples herdando de `QWidget` ou `QFrame`.
- Inclui um bloco de estilo QSS isolado opcional.

### `fleting create model <nome>`
Gera um arquivo com uma `dataclass` ou classe de dados pura.

---

## ▶️ Executando o Projeto

```bash
fleting run
# ou
python main.py
```

O comando `fleting run` deve:
1. Validar se as dependências do `PySide6` estão instaladas.
2. Iniciar o processo do `main.py`.
3. Capturar logs de erros do Qt e exibi-los de forma amigável no terminal.

---

## 🗑️ Remoção de Arquivos

### `fleting delete page <nome>`
Remove os arquivos do trio MVC e limpa as referências no Router.

### `fleting delete component <nome>`
Remove o arquivo do componente customizado.

---

## ℹ️ Informações do Ambiente

```bash
fleting info
```

Deve mostrar a versão instalada do **PySide6** e do sistema operacional (importante para layouts de Desktop).
