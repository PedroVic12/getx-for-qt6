import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QPushButton,
    QLabel,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice


class AppThemeManager:
    """Gerencia as cores do Modo Claro e Escuro via StyleSheet (QSS)"""

    # Roxo característico do Power Apps
    PURPLE_COLOR = "#7719aa"

    LIGHT_THEME = f"""
        QMainWindow, QWidget {{ background-color: #ffffff; color: #333333; }}
        QLabel {{ color: #333333; }}
        QFrame#frame_dropzone {{
            border: 2px dashed #7719aa;
            border-radius: 8px;
            background-color: #fcfcfc;
        }}
        QPushButton {{
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px 15px;
            background-color: #ffffff;
            color: #333333;
        }}
        QPushButton:hover {{ background-color: #f0f0f0; }}
        QPushButton#btn_select_file {{
            background-color: {PURPLE_COLOR};
            color: white;
            border: none;
            font-weight: bold;
        }}
        QPushButton#btn_select_file:hover {{ background-color: #5c1384; }}
        QPushButton#btn_create:disabled {{
            background-color: #f3f2f1;
            color: #a19f9d;
            border: 1px solid #e1dfdd;
        }}
    """

    DARK_THEME = f"""
        QMainWindow, QWidget {{ background-color: #1e1e1e; color: #ffffff; }}
        QLabel {{ color: #ffffff; }}
        QFrame#frame_dropzone {{
            border: 2px dashed #a561c9;
            border-radius: 8px;
            background-color: #252526;
        }}
        QPushButton {{
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 5px 15px;
            background-color: #333333;
            color: #ffffff;
        }}
        QPushButton:hover {{ background-color: #444444; }}
        QPushButton#btn_select_file {{
            background-color: {PURPLE_COLOR};
            color: white;
            border: none;
            font-weight: bold;
        }}
        QPushButton#btn_select_file:hover {{ background-color: #8c2bc4; }}
        QPushButton#btn_create:disabled {{
            background-color: #2d2d2d;
            color: #666666;
            border: 1px solid #444444;
        }}
    """


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Obtém o diretório do arquivo Python atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(current_dir, "tela_upload.ui")

        # Carrega a UI do arquivo XML
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Não foi possível abrir {ui_file_path}: {ui_file.errorString()}")
            sys.exit(-1)

        # Carrega como widget
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Se for um QMainWindow, extrai o centralwidget
        if isinstance(self.ui, QMainWindow):
            central = self.ui.centralWidget()
            if central is None:
                print("Erro: centralwidget não encontrado no arquivo UI")
                sys.exit(-1)
            self.setCentralWidget(central)
            self.setWindowTitle(self.ui.windowTitle() or "Aplicação")
        else:
            self.setCentralWidget(self.ui)
            self.setWindowTitle("Aplicação")

        self.resize(1000, 600)

        # Estado inicial do tema (True = Dark, False = Light)
        self.is_dark_mode = False

        # Encontra os widgets por nome
        self.btn_theme = self.findChild(QPushButton, "btn_theme")
        self.btn_select_file = self.findChild(QPushButton, "btn_select_file")
        self.lbl_drop_title = self.findChild(QLabel, "lbl_drop_title")
        self.btn_create = self.findChild(QPushButton, "btn_create")

        self.apply_theme()

        # Conectar botões às funções
        if self.btn_theme:
            self.btn_theme.clicked.connect(self.toggle_theme)
        if self.btn_select_file:
            self.btn_select_file.clicked.connect(self.abrir_explorador)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(AppThemeManager.DARK_THEME)
        else:
            self.setStyleSheet(AppThemeManager.LIGHT_THEME)

    def abrir_explorador(self):
        # Filtra apenas arquivos suportados descritos na tela
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo Excel",
            "",
            "Excel / CSV (*.xlsx *.xlsb *.xls *.csv)",
        )
        if arquivo:
            # Se o usuário escolheu um arquivo, ativa o botão de Criar
            if hasattr(self, "lbl_drop_title") and self.lbl_drop_title:
                self.lbl_drop_title.setText(
                    f"Arquivo selecionado:\n{arquivo.split('/')[-1]}"
                )
            if hasattr(self, "btn_create") and self.btn_create:
                self.btn_create.setEnabled(True)
                self.btn_create.setStyleSheet(
                    "background-color: #7719aa; color: white; border: none;"
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
