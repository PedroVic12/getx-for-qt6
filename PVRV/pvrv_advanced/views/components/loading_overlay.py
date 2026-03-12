from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Fundo semi-transparente estilo Palkia
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);") 
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.loading_label = QLabel("Carregando... Por favor, aguarde.")
        self.loading_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.loading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loading_label)

        # Adiciona um GIF de loading se existir na pasta assets
        self.movie_label = QLabel()
        self.movie_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("assets/loading.gif") 
        if self.movie.isValid():
            self.movie.setScaledSize(QSize(100, 100))
            self.movie_label.setMovie(self.movie)
            self.movie.start()
            layout.addWidget(self.movie_label)

    def show_loading(self, message="Carregando..."):
        self.loading_label.setText(message)
        self.resize(self.parent().size()) # Garante que cubra o pai
        self.show()

    def hide_loading(self):
        self.hide()
