from functools import lru_cache
from pathlib import Path

from jinja2 import Template

from .serializable import Serializable

__all__ = ["Serializable", "get_template"]


@lru_cache
def get_template(path: Path):
    with open(path, "r") as f:
        data = f.read()
    return Template(
        source=data, autoescape=True, trim_blocks=True, lstrip_blocks=True,
    )
