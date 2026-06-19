from json import loads
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


def load_json(filename):
    file_path = DATA_DIR / filename
    return loads(file_path.read_text(encoding="utf-8"))
