from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .serializable import Serializable

__all__ = ["Serializable", "TEMPLATE_ENVIRONMENT"]

template_path = Path(__file__).parent

TEMPLATE_ENVIRONMENT = Environment(
    loader=FileSystemLoader(searchpath=template_path),
    autoescape=True,
)
