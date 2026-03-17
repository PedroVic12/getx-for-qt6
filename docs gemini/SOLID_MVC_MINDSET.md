# 📚 SOLID & MVC: Do React (Web) ao PySide6 (Desktop)

Este guia resume como aplicar padrões de arquitetura de alto nível em dois ecossistemas diferentes, mas que compartilham os mesmos princípios de código limpo.

---

## 🏗️ 1. O Padrão MVC (Model-View-Controller)

O MVC é a base do nosso framework. Ele separa **O QUE** o app faz de **COMO** ele aparece.

| Camada | Em React (Web) | No Nosso Framework (PySide6) |
| :--- | :--- | :--- |
| **Model** | Redux Store, Context API, ou Fetch/Axios para API. | `models/`, Banco SQLite3, Dataframes Pandas. |
| **View** | Componentes JSX (Funcionais ou Classes). | `views/`, Widgets Qt6 (`StatefulView`, `StatelessView`). |
| **Controller** | Custom Hooks (ex: `useUser`), Event Handlers. | `controllers/`, Classes Python que manipulam Signals. |

### 💡 Mindset de Transição:
No **React**, a View reage ao estado (Declarativo). No **PySide6**, o Controller avisa a View que algo mudou (Imperativo/Event-Driven), mas usando o nosso `set_state()`, trazemos o conforto do React para o Desktop.

---

## 💎 2. Princípios SOLID no Desenvolvimento

### S - Single Responsibility (Responsabilidade Única)
- **React**: Um componente não deve fazer fetch de dados, validar formulário e renderizar HTML ao mesmo tempo. Separe a lógica em um Custom Hook.
- **PySide6**: A `View` define o layout. O `Controller` valida o input. O `Model` salva no DB. Se o seu Controller tem 1000 linhas, ele está fazendo coisa demais.

### O - Open/Closed (Aberto para Extensão, Fechado para Modificação)
- **React**: Use `Composition` (passar `children`) em vez de encher um componente de `if/else` para mudar o comportamento.
- **PySide6**: Herde de `StatelessView` ou `StatefulView`. Se precisar de um novo tipo de tela, crie uma nova classe em vez de modificar a `BaseView`.

### L - Liskov Substitution (Substituição de Liskov)
- **Princípio**: Uma subclasse deve poder substituir sua classe base sem quebrar o app.
- **Aplicação**: No nosso template, qualquer página que você criar herda de `StatefulView`. O `Router` não precisa saber *qual* página é, ele só precisa saber que ela tem o método `show()`.

### I - Interface Segregation (Segregação de Interface)
- **React**: Não passe props gigantescas para um componente se ele só usa o `name`.
- **PySide6**: No Controller, não force a View a implementar métodos que ela não precisa. Use **Signals** para que a View "escute" apenas o que lhe interessa.

### D - Dependency Inversion (Inversão de Dependência)
- **Princípio**: Dependa de abstrações, não de implementações concretas.
- **Aplicação**: O seu `Controller` não deve "instanciar" um banco de dados fixo. Ele deve receber a conexão (como fazemos no `get_connection()`), permitindo que você troque SQLite por PostgreSQL no futuro sem mudar a lógica do Dashboard.

---

## 🚀 Checklist de Estudo para a Equipe

1. [ ] **MVC**: Consigo explicar a diferença entre Controller e Model para um leigo?
2. [ ] **React vs Qt**: Entendo que `set_state` no Qt6 é uma abstração para `label.setText()`?
3. [ ] **Clean Code**: Minhas views têm apenas código de interface (CSS/Layout)?
4. [ ] **Persistência**: Minha lógica de banco de dados está isolada ou espalhada nos botões?

> 📖 **Leitura Recomendada**: Explore a pasta `gemini/` para entender como implementamos esses conceitos de forma prática no nosso Template de Elite.
