from pathlib import Path

root = Path(__file__).resolve().parent.parent

def get_path(*path_parts):
    return str(root / Path(*path_parts))