import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MainWindow(QMainWindow):
    def __init__(self, ui_file_path):
        super().__init__()
        loader = QUiLoader()
        file = QFile(ui_file_path)
        if not file.open(QFile.ReadOnly):
            print(f"Não foi possível abrir o arquivo UI: {ui_file_path}")
            sys.exit(-1)
        self.ui = loader.load(file, self)
        file.close()
        
        self.setCentralWidget(self.ui.centralWidget())
        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.size())
        self.setStyleSheet(self.ui.styleSheet())

        # Conectar widgets da UI
        self.btn_click = self.ui.findChild(QPushButton, "btn_click")
        self.lbl_title = self.ui.findChild(QLabel, "lbl_title")
        self.txt_input = self.ui.findChild(QLineEdit, "txt_input")

        if self.btn_click:
            self.btn_click.clicked.connect(self.on_btn_click)

    def on_btn_click(self):
        text = self.txt_input.text() if self.txt_input else ""
        if text:
            self.lbl_title.setText(f"Texto recebido: {text}")
        else:
            self.lbl_title.setText("Por favor, digite algo!")

def main():
    app = QApplication(sys.argv)
    
    ui_path = os.path.join(os.path.dirname(__file__), 'views', 'mainwindow.ui')
    window = MainWindow(ui_path)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
