print("Ferramentas Elétricas GUI")

import os
import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from repository import SIMULADORES_CONFIG

class CustomWebPage(QWebEnginePage):
    """Intercepta links que tentam abrir em nova aba (target='_blank') e abre na mesma janela."""

    def createWindow(self, _type):
        return self


class EngineeringHubWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering & Simulation Hub — PyQt6 WebEngine")
        self.resize(1440, 860)

        # Perfil persistente em disco (mantém logins do Tinkercad / CircuitVerse salvos)
        storage_path = os.path.join(os.path.expanduser("~"), ".eng_hub_webprofile")
        os.makedirs(storage_path, exist_ok=True)
        self.profile = QWebEngineProfile("EngHubProfile", self)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )

        self._setup_ui()
        self._apply_dark_theme()
        self._carregar_lista_simuladores()

        # Seleciona o primeiro item automaticamente ao abrir
        if self.menu_list.count() > 0:
            self.menu_list.setCurrentRow(0)

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ----------------------------------------------------------------------
        # 1. MENU LATERAL (Sidebar)
        # ----------------------------------------------------------------------
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setMinimumWidth(250)
        sidebar.setMaximumWidth(340)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 16, 12, 12)
        sidebar_layout.setSpacing(10)

        lbl_titulo = QLabel("⚡ SIMULATION HUB")
        lbl_titulo.setFont(QFont("Sans Serif", 13, QFont.Weight.Bold))
        lbl_titulo.setObjectName("SidebarTitle")
        sidebar_layout.addWidget(lbl_titulo)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filtrar simulador...")
        self.search_input.textChanged.connect(self._filtrar_menu)
        sidebar_layout.addWidget(self.search_input)

        self.menu_list = QListWidget()
        self.menu_list.setObjectName("MenuList")
        self.menu_list.currentItemChanged.connect(self._ao_selecionar_simulador)
        sidebar_layout.addWidget(self.menu_list)

        self.lbl_desc = QLabel("Selecione uma ferramenta acima.")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setObjectName("DescLabel")
        sidebar_layout.addWidget(self.lbl_desc)

        # ----------------------------------------------------------------------
        # 2. ÁREA PRINCIPAL (Barra de Navegação + QWebEngineView)
        # ----------------------------------------------------------------------
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Barra superior estilo navegador
        navbar = QFrame()
        navbar.setObjectName("Navbar")
        navbar.setFixedHeight(44)
        nav_layout = QHBoxLayout(navbar)
        nav_layout.setContentsMargins(8, 4, 8, 4)
        nav_layout.setSpacing(6)

        self.btn_back = QPushButton("◀")
        self.btn_forward = QPushButton("▶")
        self.btn_reload = QPushButton("↻")
        self.btn_home = QPushButton("⌂ Reset Simulador")
        self.btn_toggle_menu = QPushButton("☰ Menu")

        for btn in (self.btn_back, self.btn_forward, self.btn_reload):
            btn.setFixedWidth(32)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Digite uma URL ou selecione no menu...")
        self.url_bar.returnPressed.connect(self._navegar_url_digitada)

        nav_layout.addWidget(self.btn_toggle_menu)
        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addWidget(self.btn_reload)
        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.url_bar)

        # Barra de progresso de carregamento
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(3)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)

        # WebView (Equivalente ao iframe em tela cheia dentro do Qt6)
        self.webview = QWebEngineView()
        self.web_page = CustomWebPage(self.profile, self.webview)
        self.webview.setPage(self.web_page)

        # Habilita recursos avançados necessários para WebGL/Canvas (Falstad, Tinkercad, TryQt)
        settings = self.webview.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True
        )

        # Conexões de eventos do navegador
        self.btn_back.clicked.connect(self.webview.back)
        self.btn_forward.clicked.connect(self.webview.forward)
        self.btn_reload.clicked.connect(self.webview.reload)
        self.btn_home.clicked.connect(self._recarregar_simulador_atual)
        self.btn_toggle_menu.clicked.connect(
            lambda: sidebar.setVisible(not sidebar.isVisible())
        )

        self.webview.urlChanged.connect(lambda qurl: self.url_bar.setText(qurl.toString()))
        self.webview.loadProgress.connect(self._atualizar_progresso)

        content_layout.addWidget(navbar)
        content_layout.addWidget(self.progress_bar)
        content_layout.addWidget(self.webview)

        splitter.addWidget(sidebar)
        splitter.addWidget(content_frame)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)

    def _carregar_lista_simuladores(self):
        self.menu_list.clear()
        for nome, dados in SIMULADORES_CONFIG.items():
            item = QListWidgetItem(f"{nome}\n   [{dados['categoria']}]")
            item.setData(Qt.ItemDataRole.UserRole, nome)
            self.menu_list.addItem(item)

    def _filtrar_menu(self, texto: str):
        termo = texto.lower().strip()
        for i in range(self.menu_list.count()):
            item = self.menu_list.item(i)
            nome = item.data(Qt.ItemDataRole.UserRole)
            cat = SIMULADORES_CONFIG[nome]["categoria"]
            visivel = termo in nome.lower() or termo in cat.lower()
            item.setHidden(not visivel)

    def _ao_selecionar_simulador(self, current: QListWidgetItem, _previous):
        if not current:
            return
        nome = current.data(Qt.ItemDataRole.UserRole)
        dados = SIMULADORES_CONFIG[nome]
        self.lbl_desc.setText(f"ℹ️ {dados['descricao']}")
        self.webview.setUrl(QUrl(dados["url"]))

    def _recarregar_simulador_atual(self):
        current = self.menu_list.currentItem()
        if current:
            nome = current.data(Qt.ItemDataRole.UserRole)
            self.webview.setUrl(QUrl(SIMULADORES_CONFIG[nome]["url"]))

    def _navegar_url_digitada(self):
        url = self.url_bar.text().strip()
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.webview.setUrl(QUrl(url))

    def _atualizar_progresso(self, valor: int):
        self.progress_bar.setValue(valor)
        self.progress_bar.setVisible(valor < 100)

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #12151C;
                color: #E2E8F0;
            }
            #Sidebar {
                background-color: #181C25;
                border-right: 1px solid #2D3748;
            }
            #SidebarTitle {
                color: #38BDF8;
                padding-bottom: 4px;
            }
            QLineEdit {
                background-color: #0F172A;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 6px 10px;
                color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 1px solid #38BDF8;
            }
            #MenuList {
                background-color: transparent;
                border: none;
                outline: none;
            }
            #MenuList::item {
                background-color: #1E2430;
                border: 1px solid #2A3241;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 6px;
                color: #E2E8F0;
            }
            #MenuList::item:selected {
                background-color: #0284C7;
                border: 1px solid #38BDF8;
                color: #FFFFFF;
                font-weight: bold;
            }
            #MenuList::item:hover:!selected {
                background-color: #262E3D;
            }
            #DescLabel {
                background-color: #0F172A;
                border: 1px solid #2A3241;
                border-radius: 6px;
                padding: 8px;
                color: #94A3B8;
                font-size: 11px;
            }
            #Navbar {
                background-color: #181C25;
                border-bottom: 1px solid #2D3748;
            }
            QPushButton {
                background-color: #262E3D;
                border: 1px solid #334155;
                border-radius: 5px;
                padding: 5px 10px;
                color: #E2E8F0;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #38BDF8;
            }
            QProgressBar {
                background-color: #181C25;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #38BDF8;
            }
        """)


if __name__ == "__main__":
    # Flag útil no Linux/AMD Radeon para garantir aceleração gráfica WebGL suave
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--enable-webgl --ignore-gpu-blocklist")

    app = QApplication(sys.argv)
    window = EngineeringHubWindow()
    window.show()
    sys.exit(app.exec())
