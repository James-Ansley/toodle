import os
from base64 import b64encode
from pathlib import Path


def resolve_file(target: Path, data):
    if isinstance(data, str):
        return data
    return (target.parent / data["file"]).read_text()


def resolve_directory(target: Path, data):
    if isinstance(data, list):
        return data
    root = target.parent / data["file"]
    paths = [root / f for f in os.listdir(root)]
    return [to_bs4_file(p) for p in paths]


def to_bs4_file(path: Path):
    return {"name": path.name, "data": as_bs4(path)}


def as_bs4(path: Path):
    return b64encode(path.read_bytes()).decode()
