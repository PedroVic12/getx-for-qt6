# 🏗️ Arquitetura PySide6 MVC (Inspirada no Fleting)

Este documento descreve como o framework Qt6 (PySide6) será estruturado para suportar o padrão MVC através da CLI.

## 📁 Estrutura de Pastas do Projeto Gerado

```text
projeto/
├── assets/             # Ícones (.png), Estilos (.qss), Imagens
├── core/               # Núcleo do framework (Classes Base)
│   ├── base_view.py    # QWidget com métodos de estilização e layout
│   ├── router.py       # QStackedWidget para navegação entre páginas
│   ├── thread_worker.py # QObject/QThread genérico para tarefas em background
│   └── app.py          # QApplication configurada
├── controllers/        # Lógica: Conecta View ao Model e gerencia Signals
├── models/             # Dados: Classes de dados, integração com DB ou Pandas
├── views/
│   ├── layouts/        # Estruturas reutilizáveis (ex: Sidebar, TopBar)
│   ├── components/     # Widgets customizados (ex: LoadingOverlay, CustomButton)
│   └── pages/          # Telas completas (geradas pela CLI)
├── main.py             # Ponto de entrada (Boot do QApplication)
└── style.qss           # Estilização global via Qt Style Sheets (CSS)
```

## 🧩 Camadas de Responsabilidade

### 1. Model (Dados)
- Não conhece a interface.
- Pode ser uma `dataclass`, um `SQLAlchemy model` ou um processador de `DataFrame` (como no Palkia).
- Responsável por salvar/carregar dados do disco ou banco.

### 2. View (UI)
- Responsável apenas pelo layout e instanciar Widgets.
- Recebe o **Controller** no construtor.
- Conecta os eventos (clicks, text_changed) aos métodos do Controller.
- Exemplo: `self.btn.clicked.connect(self.controller.handle_click)`

### 3. Controller (Lógica)
- Gerencia o estado da View.
- Instancia o **Worker** para tarefas demoradas (como extração de PDFs).
- Emite Signals para atualizar a View com resultados parciais ou finais.
- Faz a ponte entre os dados brutos do Model e a exibição na View.

## 🚦 Navegação (Router)
Diferente do Flet (Web), no Qt6 usamos um `QStackedWidget` dentro de um `QMainWindow`. A CLI deve registrar novas páginas no arquivo de configuração de rotas que o `Router` lerá para alternar as telas (`setCurrentIndex`).
