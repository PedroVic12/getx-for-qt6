import json
import os

class POOModel:
    """Model para gerenciamento do progresso de estudo em POO Poliglota & QML."""

    def __init__(self, data_file: str = "poo_checklist.json"):
        self.data_file = data_file
        self.default_topics = [
            {"id": 1, "modulo": "Módulo 1", "titulo": "Variáveis, Tipos e Controle de Fluxo (C++, Python, Julia, Lua, C)", "concluido": True},
            {"id": 2, "modulo": "Módulo 2", "titulo": "Funções, Lambdas e Multiple Dispatch (Julia vs C++/Python)", "concluido": True},
            {"id": 3, "modulo": "Módulo 3", "titulo": "Classes, Structs e Encapsulamento (C++, Python, Julia, Lua)", "concluido": True},
            {"id": 4, "modulo": "Módulo 4", "titulo": "Herança, Polimorfismo e Interfaces/Traits", "concluido": False},
            {"id": 5, "modulo": "Módulo 5", "titulo": "Integração QML + Python (QObject, @Slot, Signal, Data-Binding)", "concluido": True},
            {"id": 6, "modulo": "Módulo 6", "titulo": "Matemática Aplicada em Python (Newton-Raphson & Matrizes)", "concluido": True},
            {"id": 7, "modulo": "Módulo 7", "titulo": "Matemática Aplicada em Julia (Sistemas Lineares Ax=b & Integração)", "concluido": True},
            {"id": 8, "modulo": "Módulo 8", "titulo": "Scripts Utilitários em Lua para a Rotina Diária", "concluido": True}
        ]
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.topics = json.load(f)
            except Exception:
                self.topics = self.default_topics
        else:
            self.topics = self.default_topics
            self.save_data()

    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.topics, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar progresso POO: {e}")

    def toggle_topic(self, index: int) -> bool:
        if 0 <= index < len(self.topics):
            self.topics[index]["concluido"] = not self.topics[index]["concluido"]
            self.save_data()
            return True
        return False
