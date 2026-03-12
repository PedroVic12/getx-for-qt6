#!/bin/bash

# Uso: ./fleting_pyside6_scaffold.sh meu_projeto home settings dashboard
PROJECT_NAME=$1
shift
PAGES=$@

echo "🛠️ Criando projeto $PROJECT_NAME com as páginas: $PAGES"

# 1. Cria o projeto base (reutilizando o script anterior)
chmod +x create_qt6_mvc_app.sh
./create_qt6_mvc_app.sh $PROJECT_NAME

cd $PROJECT_NAME

# 2. Loop para criar cada página MVC
for page in $PAGES; do
    if [ "$page" == "home" ]; then continue; fi # Home já é criada pelo init
    
    echo "📄 Gerando página: $page"
    
    # Capitalização para o nome da classe
    CLASS_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${page:0:1})${page:1}"
    
    # Criar Model
    cat <<EOF > models/${page}_model.py
class ${CLASS_NAME}Model:
    def __init__(self):
        self.data = {}
EOF

    # Criar Controller
    cat <<EOF > controllers/${page}_controller.py
from PySide6.QtCore import QObject

class ${CLASS_NAME}Controller(QObject):
    def __init__(self):
        super().__init__()

    def get_title(self):
        return "${CLASS_NAME} Page"
EOF

    # Criar View
    cat <<EOF > views/pages/${page}_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from controllers.${page}_controller import ${CLASS_NAME}Controller

class ${CLASS_NAME}View(QWidget):
    def __init__(self, router=None):
        super().__init__()
        self.router = router
        self.controller = ${CLASS_NAME}Controller()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Visualizando Página: ${CLASS_NAME}")
        label.setStyleSheet("font-size: 24px;")
        layout.addWidget(label)
EOF

    # Registrar Rota no configs/routes.py
    # Usando sed para inserir a nova rota na lista ROUTES
    sed -i "/ROUTES = \[/a \    { "path": "/$page", "view_class": "${CLASS_NAME}View", "module": "views.pages.${page}_view", "label": "$CLASS_NAME" }," configs/routes.py
done

echo "🎉 Projeto $PROJECT_NAME configurado com PySide6 MVC e $# páginas."
