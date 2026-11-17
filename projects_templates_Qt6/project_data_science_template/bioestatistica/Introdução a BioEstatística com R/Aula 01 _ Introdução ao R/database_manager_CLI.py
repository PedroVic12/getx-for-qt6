#!/usr/bin/env python3
import argparse
import sqlite3
import subprocess
import sys
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

# ==============================================================================
# CONFIGURAÇÃO RÁPIDA (EDITE AQUI NO NANO SE QUISER)
# ==============================================================================
PASTA_DATASETS = "."                         # Pasta raiz onde estão os CSVs e XLSXs
BANCO_SQLITE = "bioestatistica_datasets.db"  # Arquivo SQLite3 local
SCRIPT_GRAFICOS = "script_bicos_passarinhos.py"
# ==============================================================================


class DatasetLoader:
    """Responsável por descobrir e carregar arquivos CSV e XLSX usando apenas listas indexadas."""

    def __init__(self, pasta_base: str = PASTA_DATASETS):
        self.pasta_base = Path(pasta_base).resolve()
        self.arquivos_encontrados: list[Path] = []

    def escanear_arquivos(self) -> list[Path]:
        if not self.pasta_base.exists():
            raise FileNotFoundError(f"Pasta '{self.pasta_base}' não encontrada.")

        arquivos_csv = list(self.pasta_base.rglob("*.csv"))
        arquivos_xlsx = list(self.pasta_base.rglob("*.xlsx"))
        self.arquivos_encontrados = sorted(arquivos_csv + arquivos_xlsx)
        return self.arquivos_encontrados

    def obter_por_indice(self, indice: int) -> Path:
        if indice < 0 or indice >= len(self.arquivos_encontrados):
            raise IndexError(f"Índice {indice} fora do intervalo (0 a {len(self.arquivos_encontrados) - 1}).")
        return self.arquivos_encontrados[indice]

    def ler_dataframe(self, caminho: Path) -> pd.DataFrame:
        extensao = caminho.suffix.lower()
        if extensao == ".csv":
            df = pd.read_csv(caminho, sep=None, engine="python")
            for col in df.columns:
                if df[col].dtype == object:
                    try:
                        df[col] = pd.to_numeric(df[col].str.replace(",", "."))
                    except (ValueError, TypeError):
                        pass
            return df

        if extensao == ".xlsx":
            return pd.read_excel(caminho)

        raise ValueError(f"Formato '{extensao}' não suportado. Use .csv ou .xlsx.")


class DatasetRepository:
    """Gerencia persistência, consulta e exportação de datasets no SQLite3."""

    def __init__(self, db_path: str = BANCO_SQLITE):
        self.db_path = Path(db_path).resolve()

    def _conectar(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def salvar_dataframe(self, df: pd.DataFrame, nome_tabela: str, modo: str = "replace") -> None:
        nome_limpo = "".join(c if c.isalnum() or c == "_" else "_" for c in nome_tabela.lower())
        with self._conectar() as conn:
            df.to_sql(nome_limpo, conn, if_exists=modo, index=False)

    def listar_tabelas(self) -> list[str]:
        with self._conectar() as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            return [linha[0] for linha in cursor.fetchall()]

    def ler_tabela(self, nome_tabela: str, limite: int = 10) -> pd.DataFrame:
        with self._conectar() as conn:
            query = f"SELECT * FROM '{nome_tabela}' LIMIT {int(limite)};"
            return pd.read_sql_query(query, conn)

    def executar_sql(self, query: str) -> pd.DataFrame:
        with self._conectar() as conn:
            return pd.read_sql_query(query, conn)

    def exportar_tabela(self, nome_tabela: str, destino: Path) -> None:
        with self._conectar() as conn:
            df = pd.read_sql_query(f"SELECT * FROM '{nome_tabela}';", conn)

        if destino.suffix.lower() == ".xlsx":
            df.to_excel(destino, index=False)
        else:
            df.to_csv(destino, index=False, sep=";")


class DatasetManagerCLI:
    """Interface CLI com Rich Panel para navegação por índice e operação no SQLite3."""

    def __init__(self, pasta: str, db_path: str):
        self.console = Console()
        self.loader = DatasetLoader(pasta)
        self.repo = DatasetRepository(db_path)
        self.df_atual: pd.DataFrame | None = None
        self.arquivo_atual: Path | None = None

    def exibir_painel_arquivos(self) -> list[Path]:
        arquivos = self.loader.escanear_arquivos()
        tabela = Table(show_header=True, header_style="bold cyan", expand=True)
        tabela.add_column("Índice", justify="center", style="bold yellow", width=8)
        tabela.add_column("Arquivo", style="bold white")
        tabela.add_column("Tipo", justify="center", style="green", width=8)
        tabela.add_column("Pasta Relativa", style="dim")

        for idx, arq in enumerate(arquivos):
            rel = arq.parent.relative_to(self.loader.pasta_base)
            pasta_str = "." if str(rel) == "." else str(rel)
            tabela.add_row(str(idx), arq.name, arq.suffix.upper(), pasta_str)

        painel = Panel(
            tabela if arquivos else "[red]Nenhum arquivo .csv ou .xlsx encontrado nesta pasta.[/red]",
            title=f"[bold green]Datasets Disponíveis em: {self.loader.pasta_base}[/bold green]",
            subtitle=f"Total: {len(arquivos)} arquivo(s) | Banco SQLite: {self.repo.db_path.name}",
            border_style="bright_blue",
        )
        self.console.print(painel)
        return arquivos

    def exibir_painel_tabelas_sqlite(self) -> list[str]:
        tabelas = self.repo.listar_tabelas()
        tabela_ui = Table(show_header=True, header_style="bold magenta", expand=True)
        tabela_ui.add_column("Índice", justify="center", style="bold yellow", width=8)
        tabela_ui.add_column("Tabela no SQLite3", style="bold white")

        for idx, nome in enumerate(tabelas):
            tabela_ui.add_row(str(idx), nome)

        painel = Panel(
            tabela_ui if tabelas else "[yellow]Nenhuma tabela gravada no SQLite3 ainda.[/yellow]",
            title=f"[bold magenta]Tabelas no Banco SQLite3 ({self.repo.db_path.name})[/bold magenta]",
            border_style="magenta",
        )
        self.console.print(painel)
        return tabelas

    def exibir_preview_dataframe(self, df: pd.DataFrame, titulo: str) -> None:
        tabela_preview = Table(show_header=True, header_style="bold green", expand=True)
        for col in df.columns:
            tabela_preview.add_column(str(col), overflow="fold")

        for _, linha in df.head(5).iterrows():
            tabela_preview.add_row(*[str(v) for v in linha.values])

        info = f"Linhas: [bold]{df.shape[0]}[/bold] | Colunas: [bold]{df.shape[1]}[/bold] -> {list(df.columns)}"
        self.console.print(
            Panel(
                tabela_preview,
                title=f"[bold cyan]{titulo}[/bold cyan]",
                subtitle=info,
                border_style="cyan",
            )
        )

    def selecionar_arquivo_por_indice(self) -> None:
        arquivos = self.exibir_painel_arquivos()
        if not arquivos:
            return

        indice = IntPrompt.ask(
            "[bold yellow]Digite o número de índice do dataset[/bold yellow]",
            default=0,
        )
        try:
            caminho = self.loader.obter_por_indice(indice)
            self.df_atual = self.loader.ler_dataframe(caminho)
            self.arquivo_atual = caminho
            self.exibir_preview_dataframe(self.df_atual, f"Carregado [{indice}]: {caminho.name}")
        except (IndexError, ValueError) as exc:
            self.console.print(f"[bold red][ERRO][/bold red] {exc}")

    def importar_atual_para_sqlite(self) -> None:
        if self.df_atual is None or self.arquivo_atual is None:
            self.console.print("[yellow]Selecione um dataset pelo índice primeiro (opção 1).[/yellow]")
            return

        nome_padrao = self.arquivo_atual.stem
        nome_tabela = Prompt.ask("Nome da tabela no SQLite3", default=nome_padrao)
        self.repo.salvar_dataframe(self.df_atual, nome_tabela, modo="replace")
        self.console.print(
            Panel(
                f"Dataset [bold]{self.arquivo_atual.name}[/bold] salvo na tabela [bold green]{nome_tabela}[/bold green] ({len(self.df_atual)} linhas).",
                title="[bold green]Sucesso no SQLite3[/bold green]",
                border_style="green",
            )
        )

    def inspecionar_ou_exportar_sqlite(self) -> None:
        tabelas = self.exibir_painel_tabelas_sqlite()
        if not tabelas:
            return

        indice = IntPrompt.ask("[bold yellow]Digite o índice da tabela SQLite3[/bold yellow]", default=0)
        if indice < 0 or indice >= len(tabelas):
            self.console.print("[bold red]Índice inválido.[/bold red]")
            return

        nome_tabela = tabelas[indice]
        df_tab = self.repo.ler_tabela(nome_tabela, limite=10)
        self.exibir_preview_dataframe(df_tab, f"Preview SQLite [{indice}]: {nome_tabela}")

        acao = Prompt.ask(
            "Ação na tabela: [1] Exportar CSV  [2] Exportar XLSX  [3] Rodar SQL customizado  [0] Voltar",
            choices=["0", "1", "2", "3"],
            default="0",
        )
        if acao == "1":
            destino = Path(f"{nome_tabela}_export.csv")
            self.repo.exportar_tabela(nome_tabela, destino)
            self.console.print(f"[green]Exportado para {destino}[/green]")
        elif acao == "2":
            destino = Path(f"{nome_tabela}_export.xlsx")
            self.repo.exportar_tabela(nome_tabela, destino)
            self.console.print(f"[green]Exportado para {destino}[/green]")
        elif acao == "3":
            sql = Prompt.ask("Digite a query SQL", default=f"SELECT * FROM {nome_tabela} LIMIT 5;")
            try:
                res = self.repo.executar_sql(sql)
                self.exibir_preview_dataframe(res, "Resultado da Query SQL")
            except sqlite3.Error as err:
                self.console.print(f"[bold red][ERRO SQL][/bold red] {err}")

    def abrir_no_script_graficos(self) -> None:
        if self.arquivo_atual is None:
            self.console.print("[yellow]Selecione um dataset pelo índice primeiro (opção 1).[/yellow]")
            return

        script_path = Path(SCRIPT_GRAFICOS)
        if not script_path.exists():
            self.console.print(f"[red]Script '{SCRIPT_GRAFICOS}' não encontrado na pasta atual.[/red]")
            return

        engine = Prompt.ask("Biblioteca", choices=["pandas", "matplotlib", "seaborn", "plotly"], default="plotly")
        subtipo = Prompt.ask("Subtipo", choices=["scatter", "line", "bar", "hist", "box", "3d"], default="scatter")
        cmd = [sys.executable, str(script_path), "-f", str(self.arquivo_atual), "-t", engine, "-s", subtipo]
        subprocess.run(cmd, check=False)

    def executar_menu_interativo(self) -> None:
        while True:
            status_atual = self.arquivo_atual.name if self.arquivo_atual else "Nenhum"
            menu_texto = (
                f"[bold cyan]Dataset ativo:[/bold cyan] [bold white]{status_atual}[/bold white]\n\n"
                "[bold yellow][1][/bold yellow] Listar e escolher dataset (CSV/XLSX) por índice\n"
                "[bold yellow][2][/bold yellow] Salvar dataset ativo no banco SQLite3\n"
                "[bold yellow][3][/bold yellow] Listar/Consultar/Exportar tabelas do SQLite3 por índice\n"
                "[bold yellow][4][/bold yellow] Plotar dataset ativo no script de gráficos\n"
                "[bold yellow][0][/bold yellow] Sair"
            )
            self.console.print(
                Panel(
                    menu_texto,
                    title="[bold bright_blue]Gerenciador POO de Datasets + SQLite3[/bold bright_blue]",
                    border_style="bright_blue",
                )
            )

            opcao = Prompt.ask("Escolha uma opção", choices=["0", "1", "2", "3", "4"], default="1")
            if opcao == "0":
                self.console.print("[bold green]Encerrando CLI.[/bold green]")
                break
            elif opcao == "1":
                self.selecionar_arquivo_por_indice()
            elif opcao == "2":
                self.importar_atual_para_sqlite()
            elif opcao == "3":
                self.inspecionar_ou_exportar_sqlite()
            elif opcao == "4":
                self.abrir_no_script_graficos()


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerenciador POO de datasets CSV/XLSX com SQLite3 e Rich CLI.")
    parser.add_argument("-p", "--pasta", default=PASTA_DATASETS, help="Pasta raiz para buscar CSV e XLSX")
    parser.add_argument("-db", "--database", default=BANCO_SQLITE, help="Caminho do banco SQLite3")
    parser.add_argument("-i", "--interativo", action="store_true", help="Abre o menu interativo com Rich Panel")
    parser.add_argument("--index", type=int, default=None, help="Seleciona direto um arquivo pelo índice numérico")
    parser.add_argument("--import-sqlite", action="store_true", help="Importa o arquivo do --index direto para o SQLite3")

    args = parser.parse_args()
    cli = DatasetManagerCLI(pasta=args.pasta, db_path=args.database)

    if args.interativo:
        cli.executar_menu_interativo()
        return

    arquivos = cli.exibir_painel_arquivos()
    if args.index is not None and arquivos:
        caminho = cli.loader.obter_por_indice(args.index)
        df = cli.loader.ler_dataframe(caminho)
        cli.exibir_preview_dataframe(df, f"Dataset [{args.index}]: {caminho.name}")
        if args.import_sqlite:
            cli.repo.salvar_dataframe(df, caminho.stem)
            cli.console.print(f"[bold green]Salvo no SQLite3 como '{caminho.stem}'![/bold green]")


if __name__ == "__main__":
    main()
