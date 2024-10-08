import json
import os

from mango_ui.models.models import ThemeConfig
with open(f'{os.path.dirname(os.path.abspath(__file__))}/mango.json', "r", encoding='utf-8') as f:
    THEME = ThemeConfig(**json.loads(f.read()))
