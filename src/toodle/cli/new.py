from pathlib import Path


def new(qtype: str, name: str):
    root = Path(name)
    root.mkdir()
