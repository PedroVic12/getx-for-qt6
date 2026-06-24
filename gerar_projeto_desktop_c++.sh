#!/bin/bash

echo "========================================================="
echo "   GERADOR DE MODELOS DESKTOP HÍBRIDOS (C++ QT6 + PYTHON) "
echo "========================================================="

# 1. ESCOLA DO MODELO DE PROJETO TEMPLATE
echo "Escolha o tipo de projeto template:"
echo "1) Simulador de Engenharia e Circuitos Elétricos"
echo "2) Analisador de Séries Temporais e Dados Científicos"
echo "3) Central de Monitoramento e Automação Industrial"
read -p "Digite a opção (1, 2 ou 3): " OPT_PROJETO

case $OPT_PROJETO in
    1) NOMES_TELAS=("Análise Nodal" "Fluxo de Potência" "Matriz Y-Bus"); NOME_DIR="simulador_engenharia" ;;
    2) NOMES_TELAS=("Séries Temporais" "Previsão Demanda" "Decomposição"); NOME_DIR="analisador_dados" ;;
    3) NOMES_TELAS=("Telemetria" "Controle Motores" "Logs Sistema"); NOME_DIR="central_automacao" ;;
    *) NOMES_TELAS=("Tela Alfa" "Tela Beta" "Tela Gama"); NOME_DIR="app_hibrido_qt" ;;
esac

# 2. ESCOLHA DO TEMA VISUAL
echo -e "\nEscolha o tema visual:"
echo "1) Dark Neon (Fundo Grafite com Detalhes Ciano/Verde)"
echo "2) Matrix Code (Fundo Preto com Detalhes Verdes)"
echo "3) Cyber Light (Fundo Claro de Alta Visibilidade)"
read -p "Digite a opção (1, 2 ou 3): " OPT_TEMA

case $OPT_TEMA in
    1) BG="#1e1e24"; SIDEBAR="#121214"; TEXT="#ffffff"; ACCENT="#00ffff" ;;
    2) BG="#000000"; SIDEBAR="#0d1117"; TEXT="#00ff00"; ACCENT="#00aa00" ;;
    3) BG="#f4f6f9"; SIDEBAR="#ffffff"; TEXT="#212529"; ACCENT="#007bff" ;;
    *) BG="#1e1e24"; SIDEBAR="#121214"; TEXT="#ffffff"; ACCENT="#00ffff" ;;
esac

echo -e "\nCriando pastas padrão MVC no diretório: $NOME_DIR..."
mkdir -p "$NOME_DIR"/{backend/{models,controllers},frontend/{src/{views,controllers},build}}

# -----------------------------------------------------------------------------
# 3. CRIAÇÃO DOS ARQUIVOS DO BACKEND PYTHON + SQLITE3
# -----------------------------------------------------------------------------
cat << 'EOF' > "$NOME_DIR/backend/requirements.txt"
pandas>=2.0.0
numpy>=1.20.0
matplotlib>=3.5.0
EOF

cat << 'EOF' > "$NOME_DIR/backend/models/database.py"
import sqlite3
import os

class DatabaseModel:
    def __init__(self, db_name="dados_cientificos.db"):
        self.db_name = db_name
        self.inicializar_banco()

    def inicializar_banco(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Tabela genérica para armazenar matrizes, vetores ou telemetria
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                variavel TEXT NOT NULL,
                valor REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def salvar_leitura(self, variavel, valor):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO telemetria (variavel, valor) VALUES (?, ?)", (variavel, valor))
        conn.commit()
        conn.close()
EOF

cat << 'EOF' > "$NOME_DIR/backend/main.py"
import sys
import json
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.database import DatabaseModel

def processar_comando(linha, db):
    try:
        requisicao = json.loads(linha)
        acao = requisicao.get("acao")
        
        if acao == "CALCULAR":
            # Exemplo de lógica de processamento matemático no backend Python
            valores = requisicao.get("dados", [])
            resultado = sum(valores) * 1.05 # Simula uma amplificação ou cálculo de ganho
            
            # Salva a telemetria do cálculo no banco de dados SQLite3
            db.salvar_leitura(requisicao.get("nome_calculo", "Geral"), resultado)
            
            resposta = {"status": "sucesso", "resultado": resultado, "msg": "Calculado e Salvo no SQLite3"}
            print(json.dumps(resposta), flush=True)
            
    except Exception as e:
        print(json.dumps({"status": "erro", "mensagem": str(e)}), flush=True)

if __name__ == "__main__":
    db = DatabaseModel()
    # Loop infinito escutando as entradas vindas do processo C++ (Stdin/Stdout Pipes)
    for linha in sys.stdin:
        if not linha.strip():
            continue
        processar_comando(linha, db)
EOF

# -----------------------------------------------------------------------------
# 4. CRIAÇÃO DOS ARQUIVOS DO FRONTEND C++ QT6
# -----------------------------------------------------------------------------
cat << EOF > "$NOME_DIR/frontend/src/views/mainwindow.h"
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QPushButton>
#include <QTabWidget>
#include <QLabel>
#include <QFrame>
#include <QProcess>

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void abrirNovaAba(const QString &titulo, const QString &conteudo);
    void enviarDadosAoBackendPython();
    void lerRespostaDoPython();

private:
    QFrame *sidebar;
    QTabWidget *tabsHeader;
    QProcess *processoPython;
};

#endif // MAINWINDOW_H
EOF

cat << EOF > "$NOME_DIR/frontend/src/views/mainwindow.cpp"
#include "mainwindow.h"
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QMessageBox>
#include <QCoreApplication>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    this->resize(1024, 640);

    // Folha de Estilo Dinâmica baseada nas escolhas do Script SH
    this->setStyleSheet(
        "QMainWindow { background-color: ${BG}; }"
        "QFrame#Sidebar { background-color: ${SIDEBAR}; border-right: 2px solid ${ACCENT}; }"
        "QPushButton { color: ${TEXT}; background-color: transparent; border: 1px solid transparent; padding: 12px; text-align: left; font-size: 13px; font-weight: bold; }"
        "QPushButton:hover { background-color: ${ACCENT}; color: ${BG}; border-radius: 5px; }"
        "QTabWidget::pane { border: 1px solid ${ACCENT}; background-color: ${SIDEBAR}; }"
        "QTabBar::tab { background: ${SIDEBAR}; color: ${TEXT}; padding: 10px 20px; border: 1px solid ${ACCENT}; border-bottom: none; }"
        "QTabBar::tab:selected { background: ${ACCENT}; color: ${BG}; }"
        "QLabel { color: ${TEXT}; font-size: 15px; }"
    );

    QWidget *centralWidget = new QWidget(this);
    QHBoxLayout *mainLayout = new QHBoxLayout(centralWidget);
    this->setCentralWidget(centralWidget);

    // ---- MENU LATERAL ----
    sidebar = new QFrame(this);
    sidebar->setObjectName("Sidebar");
    QVBoxLayout *sidebarLayout = new QVBoxLayout(sidebar);
    sidebarLayout->setAlignment(Qt::AlignTop);

    QPushButton *btnTela1 = new QPushButton("📊 ${NOMES_TELAS[0]}", sidebar);
    QPushButton *btnTela2 = new QPushButton("⚡ ${NOMES_TELAS[1]}", sidebar);
    QPushButton *btnTela3 = new QPushButton("🔢 ${NOMES_TELAS[2]}", sidebar);
    QPushButton *btnCalcular = new QPushButton("🚀 Disparar Cálculo Python", sidebar);
    btnCalcular->setStyleSheet("background-color: ${ACCENT}; color: ${BG}; margin-top: 20px;");

    sidebarLayout->addWidget(btnTela1);
    sidebarLayout->addWidget(btnTela2);
    sidebarLayout->addWidget(btnTela3);
    sidebarLayout->addWidget(btnCalcular);
    mainLayout->addWidget(sidebar, 1);

    // ---- SISTEMA DE ABAS (HEADER COM IFRAMES SIMULADOS) ----
    tabsHeader = new QTabWidget(this);
    tabsHeader->setTabsClosable(true);
    connect(tabsHeader, &QTabWidget::tabCloseRequested, tabsHeader, &QTabWidget::removeTab);
    mainLayout->addWidget(tabsHeader, 4);

    // Conexões de Navegação das Telas
    connect(btnTela1, &QPushButton::clicked, [this]() { abrirNovaAba("${NOMES_TELAS[0]}", "Módulo Científico para a tela de ${NOMES_TELAS[0]} carregado."); });
    connect(btnTela2, &QPushButton::clicked, [this]() { abrirNovaAba("${NOMES_TELAS[1]}", "Painel de controle matricial de ${NOMES_TELAS[1]}."); });
    connect(btnTela3, &QPushButton::clicked, [this]() { abrirNovaAba("${NOMES_TELAS[2]}", "Ajustes analíticos de ${NOMES_TELAS[2]}."); });
    connect(btnCalcular, &QPushButton::clicked, this, &MainWindow::enviarDadosAoBackendPython);

    // Inicialização assíncrona do Pipeline do Python
    processoPython = new QProcess(this);
    connect(processoPython, &QProcess::readyReadStandardOutput, this, &MainWindow::lerRespostaDoPython);
    
    // Altere para apontar para a pasta correta do script em execução
    processoPython->start("python3", QStringList() << "../../backend/main.py");

    abrirNovaAba("Painel Principal", "Bem-vindo ao workspace do seu projeto gerado via automação.");
}

MainWindow::~MainWindow() {
    processoPython->close();
}

void MainWindow::abrirNovaAba(const QString &titulo, const QString &conteudo) {
    for (int i = 0; i < tabsHeader->count(); ++i) {
        if (tabsHeader->tabText(i) == titulo) {
            tabsHeader->setCurrentIndex(i);
            return;
        }
    }
    QWidget *novaPagina = new QWidget();
    QVBoxLayout *layoutPagina = new QVBoxLayout(novaPagina);
    layoutPagina->addWidget(new QLabel(conteudo, novaPagina));
    tabsHeader->addTab(novaPagina, titulo);
    tabsHeader->setCurrentWidget(novaPagina);
}

void MainWindow::enviarDadosAoBackendPython() {
    QJsonObject json;
    json["acao"] = "CALCULAR";
    json["nome_calculo"] = "Matriz Nodal Elétrica";
    
    QJsonArray dados;
    dados.append(10.5); dados.append(22.4); dados.append(35.1);
    json["dados"] = dados;

    QJsonDocument doc(json);
    processoPython->write(doc.toJson(QJsonDocument::Compact) + "\n");
}

void MainWindow::lerRespostaDoPython() {
    QByteArray resposta = processoPython->readAllStandardOutput().trimmed();
    QJsonDocument doc = QJsonDocument::fromJson(resposta);
    QJsonObject obj = doc.object();

    if (obj["status"].toString() == "sucesso") {
        double res = obj["resultado"].toDouble();
        QString msg = obj["msg"].toString();

QMessageBox::information(this, "Resposta do SQLite3/Python",QString("Resultado do Cálculo Processado: %1\nStatus: %2").arg(res).arg(msg));}}EOFcat << 'EOF' > "$NOME_DIR/frontend/src/main.cpp"#include #include "views/mainwindow.h"int main(int argc, char *argv[]) {QApplication app(argc, argv);MainWindow w;w.setWindowTitle("Ambiente de Desenvolvimento Científico Híbrido");w.show();return app.exec();}EOF5. GERANDO ARQUIVO DE BUILD CMAKE PARA O FRONTENDcat << 'EOF' > "$NOME_DIR/frontend/CMakeLists.txt"cmake_minimum_required(VERSION 3.16)project(AppHibridoCientifico LANGUAGES CXX)set(CMAKE_CXX_STANDARD 17)set(CMAKE_CXX_STANDARD_REQUIRED ON)set(CMAKE_AUTOMOC ON)find_package(Qt6 REQUIRED COMPONENTS Widgets)add_executable(AppHibridoCientificosrc/main.cppsrc/views/mainwindow.cppsrc/views/mainwindow.h)target_link_libraries(AppHibridoCientifico PRIVATE Qt6::Widgets)EOF-----------------------------------------------------------------------------6. FINALIZAÇÃO-----------------------------------------------------------------------------echo -e "\n---------------------------------------------------------"echo "[SUCESSO] Projeto '$NOME_DIR' estruturado em MVC!"echo "---------------------------------------------------------"echo "Para rodar o Frontend C++ no Garuda Linux:"echo "  1) cd $NOME_DIR/frontend/build"echo "  2) cmake .."echo "  3) make"echo "  4) ./AppHibridoCientifico"echo "---------------------------------------------------------"


