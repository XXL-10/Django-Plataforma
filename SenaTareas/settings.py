# filepath: /c:/laragon/www/Listado/myproject/SenaTareas/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]