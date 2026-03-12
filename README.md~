<p align="center">
| <a href="https://alexyucra.github.io/Fleting/">🇺🇸 English</a> |
  <a href="https://alexyucra.github.io/Fleting/pt/cli/">🇧🇷 Português</a> |
  <a href="https://alexyucra.github.io/Fleting/es/cli/">🇪🇸 Español</a> |
</p>

---
<p align="center">
  <img src="../img/fleting_logo.png" width="100"/>
</p>

# Fleting Framework

Fleting is an opinionated micro-framework built on top of Flet, focused on:

- Simplicity
- Clear organization
- Productivity
- Cross-platform applications (mobile, tablet, and desktop)

Ele traz uma arquitetura inspirada em MVC, com **layout desacoplado**, **roteamento simples**, **i18n**, **responsividade automática** e um **CLI para geração de código**.

It brings an MVC-inspired architecture with **decoupled layout**, **simple routing**, **i18n**, **automatic responsiveness**, and a **CLI for code generation**.

<p align="center">
  <img src="docs/img/fleting.gif" width="260" />
</p>

---

## 💎 Novas Funcionalidades (Qt6 Elite Edition)

O Fleting evoluiu! Agora, além do Flet, o framework oferece um motor de geração de código para **PySide6 (Qt6)** focado em softwares desktop de alta performance:

- **🏗️ Motor MVC Nativo**: CLI configurada para gerar projetos estruturados em Controllers, Models e Views nativas.
- **🔄 Stateful & Stateless Views**: Arquitetura de interface inspirada no Flutter (`build`, `set_state`) para máxima produtividade.
- **☰ Sidebar de Elite**: Barra lateral retrátil e responsiva com sistema de navegação por ícones e labels.
- **🌓 Dark Mode Pro**: Toggle instantâneo de temas (Sol/Lua) com estilos de alto contraste padronizados.
- **📝 Checklist Markdown**: Widget inteligente que renderiza listas complexas via Markdown com persistência automática em **SQLite3**.
- **📂 Link Áncora Inteligente**: Botão integrado na UI que abre a pasta de documentação (`gemini/**`) diretamente no explorador de arquivos do seu SO.

---

## 🚀 Quick Start

### 1. Create an isolated virtual environment

- [Recommended: environment with poetry](docs/pt/enviroment.md)


## 🛠️ CLI (Qt6 Edition)

Para utilizar o novo motor de geração de código para **PySide6**, siga os comandos abaixo:

```shell
# Instale as dependências necessárias
pip install PySide6 rich

# Inicialize um novo projeto Elite
python3 -m fleting.cli.cli init meu_projeto

# Entre na pasta e execute
cd meu_projeto
python3 main.py
```

### ⚠️ Importante: Desenvolvimento Local

Sempre que você estiver utilizando esta versão modificada do framework dentro deste repositório, utilize o comando via módulo Python para garantir que os **Templates Elite** sejam aplicados corretamente:

> **Comando Recomendado:** `python3 -m fleting.cli.cli <comando>`

Isso evita que o sistema utilize uma versão antiga do `fleting` instalada globalmente no seu ambiente.

---

## 📚 Documentation

Complete documentation is available at:

👉 [Full documentation](docs/pt/index.md)

---

## 🎯 Philosophy

O Fleting foi criado com alguns princípios claros:

### 1️⃣ Simplicity above all
- No unnecessary abstractions
- Explicit and easy-to-understand code
- Predictable architecture

### 2️⃣ Separation of responsibilities
- **View** → Pure UI (Flet)
- **Layout** → Reusable visual structure
- **Controller** → Business rules
- **Model** → Data
- **Router** → Navegação
- **Core** → Framework infrastructure

### 3️⃣ Mobile-first
- The global application state automatically identifies:
  - `mobile`
  - `tablet`
  - `desktop`
- Layouts can dynamically react to device type

### 4️⃣ Native internationalization
- Simple JSON-based translation system
- Real-time language switching
- Translations accessible anywhere in the app

### 5️⃣ CLI as a first-class citizen
- Standardized file creation and removal
- Reduced boilerplate
- Convention > Configuration

---

## 📄 License

MIT

## How to contribute
- [For those who want to contribute to Fleting on GitHub.](CONTRIBUTING.md)