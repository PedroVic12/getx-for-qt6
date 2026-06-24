import sys
import pandapower as pp
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                               QPushButton, QLabel, QMessageBox)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class AnalisadorSEP:
    """
    Classe para modelar, calcular e desenhar a rede elétrica com Pandapower,
    simulando a entrada de dados no estilo de um arquivo PWF (CEPEL).
    """
    def __init__(self):
        # Cria uma rede vazia do pandapower
        self.net = pp.create_empty_network(name="Sistema_Teste_PWF")
        self.barras_dict = {} # Para mapear nomes de barras para os índices do pandapower
        
        # Dados simulados (normalmente viriam da leitura de um arquivo .PWF ou .xlsx)
        self.dados_barras = [
            {"nome": "BARRA_GERACAO", "vn_kv": 13.8, "tipo": "b", "geocord": (0, 0)},
            {"nome": "BARRA_SUB_AT", "vn_kv": 138.0, "tipo": "b", "geocord": (2, 2)},
            {"nome": "BARRA_CARGA_1", "vn_kv": 138.0, "tipo": "b", "geocord": (5, 2)},
            {"nome": "BARRA_CARGA_2", "vn_kv": 138.0, "tipo": "b", "geocord": (5, -1)}
        ]
        
        self.dados_trafos = [
            {"nome": "TRAFO_ELEVADOR", "barra_at": "BARRA_SUB_AT", "barra_bt": "BARRA_GERACAO", 
             "sn_mva": 50.0, "vn_hv_kv": 138.0, "vn_lv_kv": 13.8, "vk_percent": 10.0, "vkr_percent": 0.5, 
             "pfe_kw": 20.0, "i0_percent": 0.1}
        ]
        
        self.dados_linhas = [
            {"nome": "LT_SUB_C1", "barra_de": "BARRA_SUB_AT", "barra_para": "BARRA_CARGA_1", 
             "length_km": 50.0, "r_ohm_per_km": 0.05, "x_ohm_per_km": 0.2, "c_nf_per_km": 10.0, "max_i_ka": 1.0},
            {"nome": "LT_C1_C2", "barra_de": "BARRA_CARGA_1", "barra_para": "BARRA_CARGA_2", 
             "length_km": 30.0, "r_ohm_per_km": 0.05, "x_ohm_per_km": 0.2, "c_nf_per_km": 10.0, "max_i_ka": 1.0}
        ]

        self.dados_cargas = [
            {"barra": "BARRA_CARGA_1", "p_mw": 15.0, "q_mvar": 5.0},
            {"barra": "BARRA_CARGA_2", "p_mw": 20.0, "q_mvar": 8.0}
        ]

    def construir_rede(self):
        """Constrói a rede Pandapower baseada nos dados fornecidos."""
        try:
            # 1. Criar Barras
            for b in self.dados_barras:
                idx = pp.create_bus(self.net, name=b["nome"], vn_kv=b["vn_kv"], 
                                    type=b["tipo"], geodata=b["geocord"])
                self.barras_dict[b["nome"]] = idx
            
            # Criar barra de folga (Slack) na geração
            pp.create_ext_grid(self.net, bus=self.barras_dict["BARRA_GERACAO"], vm_pu=1.0)

            # 2. Criar Transformadores
            for t in self.dados_trafos:
                pp.create_transformer_from_parameters(
                    self.net, 
                    hv_bus=self.barras_dict[t["barra_at"]], 
                    lv_bus=self.barras_dict[t["barra_bt"]], 
                    sn_mva=t["sn_mva"], vn_hv_kv=t["vn_hv_kv"], vn_lv_kv=t["vn_lv_kv"], 
                    vkr_percent=t["vkr_percent"], vk_percent=t["vk_percent"], 
                    pfe_kw=t["pfe_kw"], i0_percent=t["i0_percent"], name=t["nome"]
                )

            # 3. Criar Linhas de Transmissão
            for l in self.dados_linhas:
                pp.create_line_from_parameters(
                    self.net, 
                    from_bus=self.barras_dict[l["barra_de"]], 
                    to_bus=self.barras_dict[l["barra_para"]], 
                    length_km=l["length_km"], r_ohm_per_km=l["r_ohm_per_km"], 
                    x_ohm_per_km=l["x_ohm_per_km"], c_nf_per_km=l["c_nf_per_km"], 
                    max_i_ka=l["max_i_ka"], name=l["nome"]
                )

            # 4. Criar Cargas
            for c in self.dados_cargas:
                pp.create_load(self.net, bus=self.barras_dict[c["barra"]], 
                               p_mw=c["p_mw"], q_mvar=c["q_mvar"])

            print("Rede construída com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao construir a rede: {e}")
            return False

    def executar_fluxo_potencia(self):
        """Roda o cálculo de fluxo de potência (Newton-Raphson)."""
        try:
            pp.runpp(self.net)
            print("Fluxo de potência convergido.")
            return True
        except pp.LoadflowNotConverged:
            print("Erro: O fluxo de potência não convergiu!")
            return False

    def desenhar_topologia(self, ax):
        """
        Desenha a rede no eixo Matplotlib fornecido, destacando os diferentes componentes.
        """
        # Limpa o eixo
        ax.clear()
        
        # Cria coleções para o gráfico
        buses = plot.create_bus_collection(self.net, size=0.2, color="blue", zorder=2)
        lines = plot.create_line_collection(self.net, use_bus_geodata=True, color="black", linewidths=2, zorder=1)
        trafos = plot.create_trafo_collection(self.net, size=0.3, color="green", zorder=2)
        ext_grids = plot.create_ext_grid_collection(self.net, size=0.5, color="orange", zorder=3)
        loads = plot.create_load_collection(self.net, size=0.3, color="red", zorder=3)

        # Adiciona ao plot
        plot.draw_collections([buses, lines, trafos, ext_grids, loads], ax=ax)
        
        # Anotações para as barras
        for idx, row in self.net.bus.iterrows():
            ax.text(row.x, row.y + 0.2, row['name'], fontsize=9, ha='center', 
                    bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1))

        ax.set_title("Diagrama Unifilar da Rede (Modelagem estilo PWF)")
        ax.set_xlabel("Coordenada X")
        ax.set_ylabel("Coordenada Y")
        ax.grid(True, linestyle='--', alpha=0.5)


class JanelaPrincipal(QMainWindow):
    """
    Interface gráfica usando PySide6 para exibir o sistema modelado.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análise de Sistema de Potência - Pandapower & POO")
        self.resize(800, 600)

        # Configurar classe de análise
        self.analisador = AnalisadorSEP()

        # Configurar UI
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout = QVBoxLayout(self.widget_central)

        self.btn_processar = QPushButton("Ler Dados, Construir Rede e Plotar")
        self.btn_processar.clicked.connect(self.processar_rede)
        
        self.lbl_status = QLabel("Aguardando ação...")

        # Configurar Matplotlib Canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.fig)

        self.layout.addWidget(self.btn_processar)
        self.layout.addWidget(self.lbl_status)
        self.layout.addWidget(self.canvas)

    def processar_rede(self):
        self.lbl_status.setText("Construindo rede e executando fluxo...")
        QApplication.processEvents()

        # 1. Constrói a rede a partir dos dados embutidos (simulando PWF)
        if self.analisador.construir_rede():
            # 2. Executa fluxo de potência
            if self.analisador.executar_fluxo_potencia():
                self.lbl_status.setText("Fluxo convergido. Desenhando...")
                # 3. Desenha no canvas
                self.analisador.desenhar_topologia(self.ax)
                self.canvas.draw()
                self.lbl_status.setText("Pronto! Diagrama unifilar gerado.")
            else:
                QMessageBox.critical(self, "Erro", "Fluxo de potência não convergiu.")
                self.lbl_status.setText("Erro de convergência.")
        else:
            QMessageBox.critical(self, "Erro", "Falha ao construir a rede.")
            self.lbl_status.setText("Erro na construção da rede.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())