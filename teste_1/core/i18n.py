import json
from pathlib import Path
class I18n:
    translations = {}
    @classmethod
    def load(cls, lang):
        path = Path("configs/languages") / f"{lang}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f: cls.translations = json.load(f)
    @classmethod
    def t(cls, key):
        v = cls.translations
        for k in key.split("."): v = v.get(k, key)
        return v
