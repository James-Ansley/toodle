from collections.abc import Mapping
from pathlib import Path

import tomli
from jinja2 import Template
from markdown import markdown

from .. import TEMPLATE_DIR

__all__ = ["parse"]

_XML_NAME = "shortanswer.xml"
_QUESTION_CONFIG = "config.toml"
_PROMPT = "prompt.md"


def parse(question_dir: Path):
    data = _get_data(question_dir)
    return _set_template(data)


def _get_data(question_dir: Path):
    with open(question_dir / _QUESTION_CONFIG, "rb") as f:
        config = tomli.load(f)
    with open(question_dir / _PROMPT) as f:
        config["prompt"] = markdown(f.read())

    config['name'] = question_dir.name
    config['case_sensitivity'] = int(config['case_sensitivity'])
    return config


def _set_template(data: Mapping):
    with open(TEMPLATE_DIR / _XML_NAME, "r") as f:
        template = Template(f.read(), trim_blocks=True, lstrip_blocks=True)
    return template.render(**data)
