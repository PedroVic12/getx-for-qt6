#!/usr/bin/env python3
"""
Dashboard Poliglota & Toolbox KDE (MVC Pattern com Qt6 QML e PySide6)
======================================================================
Este aplicativo unifica a execução de scripts poliglotas (C++, Julia, Lua, C, Python)
com a geração automática de currículos em PDF e a gestão de rotina diária Anti-Kanban.

Arquitetura MVC:
- Model: models/cv_model.py, models/routine_model.py
- View: ui/main.qml, ui/views/*.qml, ui/components/*.qml
- Controller: controllers/app_controller.py, controllers/polyglot_controller.py
"""

import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from controllers.app_controller import AppController

def main():
    # Inicializa a aplicação Qt GUI
    app = QGuiApplication(sys.argv)
    app.setOrganizationName("Batcaverna")
    app.setApplicationName("DashboardPoliglotaKDE")

    engine = QQmlApplicationEngine()

    # Instancia o Controller Principal da Arquitetura MVC
    app_controller = AppController()

    # Registra o Controller no Contexto Global do QML com a propriedade 'appController'
    engine.rootContext().setContextProperty("appController", app_controller)

    # Carrega a interface QML principal
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file = os.path.join(base_dir, "ui", "main.qml")

    print(f"🚀 Carregando interface QML de: {qml_file}")
    engine.load(qml_file)

    if not engine.rootObjects():
        print("❌ Erro ao carregar arquivo QML principal. Encerrando.")
        sys.exit(-1)

    print("✅ Aplicação MVC QML inicializada com sucesso!")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
