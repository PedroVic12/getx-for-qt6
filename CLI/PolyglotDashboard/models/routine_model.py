import json
import os

class RoutineModel:
    """Model de Gestão de Rotina Anti-Kanban (Post-it Digital de 3 itens) conforme AGENTS.md."""

    def __init__(self, data_file: str = "rotina_diaria.json"):
        self.data_file = data_file
        self.default_data = {
            "data": "2026-09-10",
            "post_its": [
                {"id": 1, "titulo": "📚 UFF: Revisão de Análise de Circuitos & EDOs", "concluido": False},
                {"id": 2, "titulo": "🏋️ Saúde: Treino de Força & 2L de Água", "concluido": True},
                {"id": 3, "titulo": "💻 Projeto: Concluir Dashboard QML Poliglota MVC", "concluido": False}
            ],
            "pomodoros_hoje": 4,
            "meta_pomodoros": 6
        }
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = self.default_data
        else:
            self.data = self.default_data
            self.save_data()

    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar rotina: {e}")

    def toggle_item(self, index: int) -> bool:
        if 0 <= index < len(self.data["post_its"]):
            self.data["post_its"][index]["concluido"] = not self.data["post_its"][index]["concluido"]
            self.save_data()
            return True
        return False

    def add_pomodoro(self) -> int:
        self.data["pomodoros_hoje"] += 1
        self.save_data()
        return self.data["pomodoros_hoje"]

    def is_expediente_finalizado(self) -> bool:
        return all(item["concluido"] for item in self.data["post_its"])
