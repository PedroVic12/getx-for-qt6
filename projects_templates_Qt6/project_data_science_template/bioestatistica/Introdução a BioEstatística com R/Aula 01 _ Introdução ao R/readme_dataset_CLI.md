
# Exemplo de uso de CLI para manejar arquivos de datasets com scripts diferentes com plots diferentes em Python, Julia, Matlab e R
---


## Uso da CLI com entrada de argumentos e tipos diferentes de graficos e interatividades

### vai ficar disṕonivel no github para quem acessar essa live! <3

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

```

---

### Como usar no terminal (sem precisar nem abrir o `nano` se não quiser)

1. **Dar permissão e rodar com o padrão definido no topo do arquivo:**
```bash
chmod +x grafico_cli.py
./grafico_cli.py

```


2. **Testar diferentes engines e a fórmula `log10(x) - log10(y)` direto por flag:**
```bash
# Gráfico interativo no Plotly com transformação log10
python grafico_cli.py -t plotly -s scatter --log

# Boxplot no Seaborn mostrando a tabela antes
python grafico_cli.py -t seaborn -s box --show

# Gráfico 3D no Plotly passando a coluna Z
python grafico_cli.py -t plotly -s 3d -z comprimento_nadadeira_mm

```

3. **Exemplos 3D avançado **
# 1. Gráfico 3D interativo (Bico x Massa x Observador)
python script_bicos_passarinhos.py -t plotly -s 3d -z observador

# 2. Mapa 3D geográfico da coleta (Longitude x Latitude x Massa Corporal)
python script_bicos_passarinhos.py -t plotly -s 3d -x Longitude -y Latitude -z massa_corporal_g

# 3. Dispersão com transformação log10(x) - log10(y) no Plotly
python script_bicos_passarinhos.py -t plotly -s scatter --log

# 4. Boxplot comparando massa corporal por observador no Seaborn
python script_bicos_passarinhos.py -t seaborn -s box -x observador -y massa_corporal_g -z None



4. **Modo loop interativo (testa vários gráficos na mesma execução sem recarregar o CSV):**
```bash
python grafico_cli.py -i

```

