# ✅ Checklist de Implementação: Framework PySide6 CLI

Este checklist serve de apoio para converter as capacidades do Flet para o seu novo motor de geração de código para PySide6.

## 🟢 Fase 1: Motor de Geração (CLI Engine)
- [ ] Mapear todos os métodos em `fleting/cli/commands/create.py`.
- [ ] Substituir o conteúdo do `fleting/cli/templates/index.py` (scaffold básico do projeto) para PySide6/Qt6.
- [ ] Criar templates de arquivos para as novas classes `BaseView`, `Router`, e `App`.
- [ ] Modificar o `register_route` para registrar classes Python do Qt em vez de views Flet.

## 🔵 Fase 2: Templates de Código (Surgical Generation)
- [ ] Template para `Page (View)`: Gerar um QWidget com `QVBoxLayout` pronto para ser populado.
- [ ] Template para `Controller`: Gerar uma classe com `__init__(self, view)` e métodos básicos de handler.
- [ ] Template para `Model`: Gerar uma `dataclass` ou classe básica de dados.
- [ ] Template para `Component`: Gerar widgets reutilizáveis (ex: botões estilizados).

## 🟣 Fase 3: UI & Palkia Features (Advanced)
- [ ] Integrar o `Worker` (Threading) no template do Controller:
    - [ ] Permitir disparar tarefas pesadas sem travar a UI (QThread).
    - [ ] Integrar `LoadingOverlay` global (como no Palkia).
- [ ] Implementar sistema de temas:
    - [ ] Ler arquivos `.qss` automaticamente.
    - [ ] Sistema de notificações globais (`NotificationManager`).
- [ ] Adicionar suporte a `PandasModel` para exibição de tabelas (QTableView).

## 🟠 Fase 4: Validação & Distribuição
- [ ] Validar o comando `fleting run` (deve chamar o main.py que inicia o QApplication).
- [ ] Atualizar as dependências no `pyproject.toml` (flet -> PySide6).
- [ ] Testar o fluxo completo: `init` -> `create page` -> `run`.
- [ ] Gerar documentação automática das classes via Docstrings.

## 🔴 Fase 5: Features de Elite (Opcional)
- [ ] Suporte a `.ui` (Qt Designer) convertido para `.py` via CLI.
- [ ] Gerador de instalador nativo (`PyInstaller` / `fbs`) via CLI.
- [ ] Sistema de logs integrados no console e arquivo (como no Palkia).
