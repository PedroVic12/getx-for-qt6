import json
from pathlib import Path

class I18n:
    translations = {}
    language = "pt"

    @classmethod
    def load(cls, lang):
        cls.language = lang
        path = Path("configs/languages") / f"{lang}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                cls.translations = json.load(f)

    @classmethod
    def t(cls, key):
        value = cls.translations
        for k in key.split("."):
            value = value.get(k, key)
            if value == key: break
        return value
