from pathlib import Path
from typing import Iterable

from jinja2 import Environment, FileSystemLoader, select_autoescape

from toodle.core.serialization.serializable import Serializable
from toodle.core.serialization.serializer import Serializer

_TEMPLATE_DIR = (Path(__file__) / ".." / "templates").resolve()


class XMLSerializer(Serializer):
    _ENVIRONMENT = Environment(
        loader=FileSystemLoader(_TEMPLATE_DIR),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    @classmethod
    def serialize(cls, target: Serializable) -> str:
        target_type = type(target).__name__.lower()
        template_name = f"{target_type}.xml"
        template = cls._ENVIRONMENT.get_template(template_name)
        return template.render(**target.serialize())

    @classmethod
    def serialize_all(cls, target: Iterable[Serializable]) -> str:
        target_type = type(target).__name__.lower()
        template_name = f"{target_type}.xml"
        template = cls._ENVIRONMENT.get_template(template_name)
        children = [cls.serialize(child) for child in target]
        return template.render(data=children)
