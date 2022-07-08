from collections.abc import Iterable

from jinja2 import Template

from .. import TEMPLATE_DIR

__all__ = ["parse"]

_XML_NAME = "category.xml"


def parse(stem: Iterable[str]):
    category = "/".join(stem)
    return _set_template(category)


def _set_template(category: str):
    with open(TEMPLATE_DIR / _XML_NAME, "r") as f:
        template = Template(f.read(), trim_blocks=True, lstrip_blocks=True)
    return template.render(category_name=category)
