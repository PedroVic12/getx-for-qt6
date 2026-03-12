# ⚔️ Flet vs PySide6 (Qt6): Comparativo de Mindset

Este documento resume as principais diferenças para quem vem do Flutter/Flet e está entrando no mundo robusto do Qt6 com PySide6.

| Característica | 🧩 Flet (Flutter Engine) | 🖼️ PySide6 (Qt6 Engine) |
| :--- | :--- | :--- |
| **Arquitetura Base** | Web/Declarativa (JSON over UDS) | Nativa/Imperativa (Direct OS drawing) |
| **Mindset de View** | Árvore de widgets imutável | Hierarquia de objetos persistentes (QObject) |
| **Thread da UI** | Flet gerencia o backend | Você gerencia o loop via `QApplication` |
| **Comunicação** | Eventos diretos no widget (`on_click`) | **Signals & Slots** (Padrão de ouro do Qt) |
| **Estilização** | Propriedades do Widget (CSS-like) | **QSS (Qt Style Sheets)** (Mais parecido com CSS real) |
| **Responsividade** | `ResponsiveRow` e `Breakpoint` | `QLayout` (VBox, HBox, Grid) + `ResizeEvent` |
| **Concorrência** | `page.run_task` ou `async` | **QThread** + **Worker** (Evita travar a UI nativa) |
| **Desempenho** | Leve para apps simples | Extremamente performático para apps de dados |

## 🚀 Como pensar em "Flutter" dentro do Qt6

- **StatelessWidget**: No Qt, é um `QWidget` onde você cria os widgets no `__init__` e eles não mudam mais de estrutura.
- **StatefulWidget**: No Qt, é um `QWidget` que possui variáveis internas. Quando você chama `set_state()`, você não reconstrói tudo, mas atualiza as propriedades dos widgets existentes (ex: `self.label.setText()`).
- **setState()**: No Flutter, você recria a view. No Qt, você usa **Signals** para avisar aos widgets que eles precisam mudar de valor.

## 🚦 Quando usar cada um?
- **Flet**: Prototipagem rápida, apps multiplataforma (Web/Mobile/Desktop) que não exigem processamento pesado local.
- **PySide6**: Softwares Desktop "pesados", dashboards com milhares de linhas, sistemas que precisam de acesso direto ao hardware ou threads intensivas (como o Palkia).
