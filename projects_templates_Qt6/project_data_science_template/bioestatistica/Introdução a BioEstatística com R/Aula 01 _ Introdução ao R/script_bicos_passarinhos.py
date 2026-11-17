#!/usr/bin/env python3
import argparse
import sys
import webbrowser
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ==============================================================================
# CONFIGURAÇÃO RÁPIDA (EDITE AQUI NO NANO E RODE: python script_bicos_passarinhos.py)
# ==============================================================================
ARQUIVO_CSV = "dados.csv"
TIPO_GRAFICO = "seaborn"               # Opções: "pandas", "matplotlib", "seaborn", "plotly"
SUBTIPO = "scatter"                    # Opções: "scatter", "line", "bar", "hist", "box", "3d"
COLUNA_X = "comprimento_do_bico_mm"
COLUNA_Y = "massa_corporal_g"
COLUNA_Z = "observador"                # Colunas reais: "observador", "Latitude", "Longitude"
USAR_LOG = False                       # True aplica: x_calc = log10(x) - log10(y)
MOSTRAR_TABELA = False                 # True imprime o resumo/head do dataset no terminal
# ==============================================================================


def carregar_dataset(caminho: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(caminho, sep=None, engine="python")
        for col in df.columns:
            if df[col].dtype == object:
                try:
                    df[col] = pd.to_numeric(df[col].str.replace(",", "."))
                except (ValueError, TypeError):
                    pass
        return df
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{caminho}' não encontrado no diretório atual.")
        sys.exit(1)


def show_datasets(df: pd.DataFrame, key: str = "df_bioestatistica1"):
    print(f"\n=== Dataset: {key} | Shape: {df.shape} ===")
    print("Colunas disponíveis:", list(df.columns))
    print("\nPrimeiras 5 linhas:")
    print(df.head())
    print("\nResumo estatístico:")
    print(df.describe())
    print("=" * 45 + "\n")


def aplicar_transformacao_log(df: pd.DataFrame, x: str, y: str) -> tuple[pd.DataFrame, str]:
    df_calc = df.dropna(subset=[x, y]).copy()
    df_calc = df_calc[(df_calc[x] > 0) & (df_calc[y] > 0)]
    nova_col_x = f"log10({x}) - log10({y})"
    df_calc[nova_col_x] = np.log10(df_calc[x]) - np.log10(df_calc[y])
    return df_calc, nova_col_x


def escolher_tipo_grafico(df: pd.DataFrame, engine: str, subtipo: str, x: str, y: str, z: str = None):
    for col in [c for c in (x, y, z) if c is not None]:
        if col not in df.columns:
            print(f"[ERRO] Coluna '{col}' não existe no CSV. Disponíveis: {list(df.columns)}")
            sys.exit(1)

    titulo = f"[{engine.upper()} - {subtipo}] {y} vs {x}"

    match engine.lower():
        case "pandas":
            kind_map = {"scatter": "scatter", "line": "line", "bar": "bar", "hist": "hist", "box": "box"}
            kind = kind_map.get(subtipo, "scatter")
            if kind in ("hist", "box"):
                df[[x, y]].plot(kind=kind, title=titulo)
            else:
                df.plot(x=x, y=y, kind=kind, title=titulo)
            plt.tight_layout()
            plt.show()

        case "matplotlib":
            fig, ax = plt.subplots(figsize=(8, 5))
            if subtipo == "line":
                ax.plot(df[x], df[y], marker="o", linestyle="-")
            elif subtipo == "bar":
                ax.bar(df[x], df[y])
            elif subtipo == "hist":
                ax.hist(df[x].dropna(), bins=20, alpha=0.7, label=x)
                ax.legend()
            else:
                ax.scatter(df[x], df[y], alpha=0.8)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(titulo)
            ax.grid(True, linestyle="--", alpha=0.4)
            plt.tight_layout()
            plt.show()

        case "seaborn":
            sns.set_theme(style="whitegrid")
            plt.figure(figsize=(8, 5))
            if subtipo == "line":
                sns.lineplot(data=df, x=x, y=y, hue=z)
            elif subtipo == "bar":
                sns.barplot(data=df, x=x, y=y, hue=z)
            elif subtipo == "box":
                sns.boxplot(data=df, x=x, y=y, hue=z)
            elif subtipo == "hist":
                sns.histplot(data=df, x=x, hue=z, kde=True)
            else:
                sns.scatterplot(data=df, x=x, y=y, hue=z)
            plt.title(titulo)
            plt.tight_layout()
            plt.show()

        case "plotly":
            if subtipo == "3d" and z:
                fig = px.scatter_3d(df, x=x, y=y, z=z, color=z, title=titulo)
            elif subtipo == "line":
                fig = px.line(df, x=x, y=y, color=z, title=titulo)
            elif subtipo == "bar":
                fig = px.bar(df, x=x, y=y, color=z, title=titulo)
            elif subtipo == "box":
                fig = px.box(df, x=x, y=y, color=z, title=titulo)
            elif subtipo == "hist":
                fig = px.histogram(df, x=x, color=z, title=titulo)
            else:
                fig = px.scatter(df, x=x, y=y, color=z, title=titulo)

            # Evita erro de pipe quebrado do Chromium zygote no Linux
            saida_html = Path("ultimo_grafico_plotly.html").resolve()
            fig.write_html(str(saida_html))
            webbrowser.open(saida_html.as_uri())

        case _:
            print(f"[ERRO] Engine '{engine}' inválida. Use: pandas, matplotlib, seaborn ou plotly.")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="CLI rápida para testar gráficos em datasets CSV.")
    parser.add_argument("-f", "--file", default=ARQUIVO_CSV, help="Caminho do arquivo CSV")
    parser.add_argument("-t", "--type", default=TIPO_GRAFICO, choices=["pandas", "matplotlib", "seaborn", "plotly"], help="Biblioteca gráfica")
    parser.add_argument("-s", "--subtipo", default=SUBTIPO, choices=["scatter", "line", "bar", "hist", "box", "3d"], help="Tipo de plot")
    parser.add_argument("-x", default=COLUNA_X, help="Coluna do eixo X")
    parser.add_argument("-y", default=COLUNA_Y, help="Coluna do eixo Y")
    parser.add_argument("-z", default=COLUNA_Z, help="Coluna Z (cor/hue ou eixo Z no Plotly 3D)")
    parser.add_argument("--log", action="store_true", default=USAR_LOG, help="Aplica x = log10(x) - log10(y)")
    parser.add_argument("--show", action="store_true", default=MOSTRAR_TABELA, help="Exibe resumo do dataset no terminal")
    parser.add_argument("-i", "--interativo", action="store_true", help="Abre menu rápido no terminal para testar vários seguidos")

    args = parser.parse_args()
    df = carregar_dataset(args.file)

    if args.show:
        show_datasets(df, key=args.file)

    if args.interativo:
        show_datasets(df, key=args.file)
        while True:
            print("Escolha rápido: [1] Pandas  [2] Matplotlib  [3] Seaborn  [4] Plotly  [5] Plotly + Log10  [0] Sair")
            op = input(">> ").strip()
            if op == "0":
                break
            mapa = {"1": ("pandas", False), "2": ("matplotlib", False), "3": ("seaborn", False), "4": ("plotly", False), "5": ("plotly", True)}
            if op in mapa:
                eng, usar_log = mapa[op]
                sub = input("Subtipo (scatter/line/bar/hist/box/3d) [Enter = scatter]: ").strip() or "scatter"
                df_plot, x_plot = aplicar_transformacao_log(df, args.x, args.y) if usar_log else (df, args.x)
                escolher_tipo_grafico(df_plot, eng, sub, x_plot, args.y, args.z)
        return

    df_plot, x_plot = aplicar_transformacao_log(df, args.x, args.y) if args.log else (df, args.x)
    escolher_tipo_grafico(df_plot, args.type, args.subtipo, x_plot, args.y, args.z)


if __name__ == "__main__":
    main()
