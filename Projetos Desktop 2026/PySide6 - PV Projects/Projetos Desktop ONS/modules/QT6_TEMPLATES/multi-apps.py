import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QStackedWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Multi-Interfaces - PySide6")
        self.resize(900, 600)

        # Widget Central e Layout Principal (Dividido entre Menu Lateral e Páginas)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # ================= MENU LATERAL (ÁRVORE) =================
        self.tree_menu = QTreeWidget()
        self.tree_menu.setHeaderHidden(True)
        self.tree_menu.setMaximumWidth(200)

        # Adicionando itens na árvore
        item_interfaces = QTreeWidgetItem(self.tree_menu, ["Interfaces"])
        self.item_tabela = QTreeWidgetItem(item_interfaces, ["1. Tabela & Exportação"])
        self.item_carrossel = QTreeWidgetItem(item_interfaces, ["2. Carrossel"])
        self.item_arquivos = QTreeWidgetItem(
            item_interfaces, ["3. Arquivos & Explorer"]
        )
        self.item_config = QTreeWidgetItem(item_interfaces, ["4. Configurações"])

        self.tree_menu.expandAll()
        main_layout.addWidget(self.tree_menu)

        # ================= ÁREA DAS PÁGINAS =================
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Criando e adicionando as 4 interfaces
        self.criar_interface_1_tabela()
        self.criar_interface_2_carrossel()
        self.criar_interface_3_arquivos()
        self.criar_interface_4_config()

        # Conectando o clique do menu à mudança de página
        self.tree_menu.itemClicked.connect(self.mudar_pagina)

    # ------------------ INTERFACE 1: Tabela e Exportações ------------------
    def criar_interface_1_tabela(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        titulo = QLabel("Tabela de Dados e Exportação")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(titulo)

        # Tabela
        self.tabela = QTableWidget(3, 3)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Status"])
        self.tabela.setItem(0, 0, QTableWidgetItem("1"))
        self.tabela.setItem(0, 1, QTableWidgetItem("Projeto Windows"))
        self.tabela.setItem(0, 2, QTableWidgetItem("Ativo"))
        layout.addWidget(self.tabela)

        # Botões de Import/Export
        btn_layout = QHBoxLayout()
        btn_import = QPushButton("Importar .md / .pwf")
        btn_exp_md = QPushButton("Exportar .MD")
        btn_exp_xlsx = QPushButton("Exportar .XLSX")
        btn_exp_pdf = QPushButton("Exportar .PDF")
        btn_exp_pwf = QPushButton("Exportar .PWF")

        # Conectando lógicas (Simulações de Diálogos)
        btn_import.clicked.connect(
            lambda: QFileDialog.getOpenFileName(
                self, "Importar Arquivo", "", "Arquivos (*.md *.pwf)"
            )
        )
        btn_exp_md.clicked.connect(lambda: self.simular_exportacao(".md"))
        btn_exp_xlsx.clicked.connect(lambda: self.simular_exportacao(".xlsx"))
        btn_exp_pdf.clicked.connect(lambda: self.simular_exportacao(".pdf"))
        btn_exp_pwf.clicked.connect(lambda: self.simular_exportacao(".pwf"))

        btn_layout.addWidget(btn_import)
        btn_layout.addWidget(btn_exp_md)
        btn_layout.addWidget(btn_exp_xlsx)
        btn_layout.addWidget(btn_exp_pdf)
        btn_layout.addWidget(btn_exp_pwf)

        layout.addLayout(btn_layout)
        self.stacked_widget.addWidget(page)

    def simular_exportacao(self, formato):
        caminho, _ = QFileDialog.getSaveFileName(
            self,
            f"Exportar como {formato}",
            "",
            f"Arquivo {formato.upper()} (*{formato})",
        )
        if caminho:
            QMessageBox.information(
                self,
                "Sucesso",
                f"Lógica de exportação para {formato} acionada!\n\nNota: Para XLSX use 'pandas', para PDF use 'reportlab'.",
            )

    # ------------------ INTERFACE 2: Carrossel ------------------
    def criar_interface_2_carrossel(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        titulo = QLabel("Carrossel de Conteúdo")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(titulo)

        # Sub-StackedWidget para agir como o Carrossel
        self.carrossel = QStackedWidget()

        # Itens do carrossel
        slide1 = QLabel("Slide 1: Bem-vindo ao Manjaro e Windows!")
        slide1.setAlignment(Qt.AlignCenter)
        slide1.setStyleSheet(
            "background-color: #2b2b2b; color: white; font-size: 20px;"
        )

        slide2 = QLabel("Slide 2: PySide6 é poderoso.")
        slide2.setAlignment(Qt.AlignCenter)
        slide2.setStyleSheet(
            "background-color: #1e3d59; color: white; font-size: 20px;"
        )

        self.carrossel.addWidget(slide1)
        self.carrossel.addWidget(slide2)
        layout.addWidget(self.carrossel)

        # Controles do Carrossel
        controles_layout = QHBoxLayout()
        btn_prev = QPushButton("<< Anterior")
        btn_next = QPushButton("Próximo >>")

        btn_prev.clicked.connect(
            lambda: self.carrossel.setCurrentIndex(
                max(0, self.carrossel.currentIndex() - 1)
            )
        )
        btn_next.clicked.connect(
            lambda: self.carrossel.setCurrentIndex(
                min(self.carrossel.count() - 1, self.carrossel.currentIndex() + 1)
            )
        )

        controles_layout.addWidget(btn_prev)
        controles_layout.addWidget(btn_next)
        layout.addLayout(controles_layout)

        self.stacked_widget.addWidget(page)

    # ------------------ INTERFACE 3: Selecionar Pasta e Abrir no Explorer ------------------
    def criar_interface_3_arquivos(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        titulo = QLabel("Gerenciador de Pastas (Windows)")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(titulo)

        self.lbl_pasta = QLabel("Nenhuma pasta selecionada.")
        self.lbl_pasta.setStyleSheet("color: gray;")
        layout.addWidget(self.lbl_pasta)

        btn_selecionar = QPushButton("Selecionar Pasta")
        btn_abrir_explorer = QPushButton("Abrir no Windows Explorer")

        # Variável para armazenar o caminho
        self.pasta_atual = ""

        def selecionar_pasta():
            pasta = QFileDialog.getExistingDirectory(self, "Selecione uma Pasta")
            if pasta:
                self.pasta_atual = os.path.normpath(pasta)
                self.lbl_pasta.setText(f"Pasta selecionada: {self.pasta_atual}")

        def abrir_explorer():
            if self.pasta_atual and os.path.exists(self.pasta_atual):
                os.startfile(
                    self.pasta_atual
                )  # Comando específico para abrir no Windows
            else:
                QMessageBox.warning(
                    self, "Aviso", "Selecione uma pasta válida primeiro."
                )

        btn_selecionar.clicked.connect(selecionar_pasta)
        btn_abrir_explorer.clicked.connect(abrir_explorer)

        layout.addWidget(btn_selecionar)
        layout.addWidget(btn_abrir_explorer)
        layout.addStretch()

        self.stacked_widget.addWidget(page)

    # ------------------ INTERFACE 4: Configurações (Simples) ------------------
    def criar_interface_4_config(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        titulo = QLabel("Configurações do Sistema")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(titulo)
        layout.addWidget(QLabel("Interface reservada para configurações futuras."))
        layout.addStretch()
        self.stacked_widget.addWidget(page)

    # ------------------ LÓGICA DE NAVEGAÇÃO DO MENU LATERAL ------------------
    def mudar_pagina(self, item):
        if item == self.item_tabela:
            self.stacked_widget.setCurrentIndex(0)
        elif item == self.item_carrossel:
            self.stacked_widget.setCurrentIndex(1)
        elif item == self.item_arquivos:
            self.stacked_widget.setCurrentIndex(2)
        elif item == self.item_config:
            self.stacked_widget.setCurrentIndex(3)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Define um estilo moderno genérico (Opcional)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
