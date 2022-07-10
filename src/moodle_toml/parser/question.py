import abc
from functools import cached_property
from pathlib import Path
from typing import Any

import tomli
from bs4 import BeautifulSoup as Soup
from jinja2 import Template
from markdown import markdown

from moodle_toml import TEMPLATE_DIR


class Question(abc.ABC):
    QUESTION_CONFIG = "config.toml"
    _PROMPT = "prompt.*"
    _XML_NAME = NotImplemented

    def __init__(self, question_dir: Path):
        self.question_dir = question_dir
        self.name = self.question_dir.name

    @cached_property
    def config(self) -> dict[str, Any]:
        path = self.question_dir / self.QUESTION_CONFIG
        with open(path, "rb") as f:
            config = tomli.load(f)
        config["prompt"] = self.prompt
        return config

    @cached_property
    def prompt(self) -> Soup:
        # ToDo - Error check for non .md or .html
        prompt_dir = next(self.question_dir.glob(self._PROMPT))
        with open(prompt_dir, "r") as f:
            prompt = f.read()
        if prompt_dir.suffix == ".md":
            prompt = markdown(prompt)
        return Soup(prompt, "html.parser")

    def as_xml(self):
        with open(TEMPLATE_DIR / self._XML_NAME, "r") as f:
            template = Template(f.read(), trim_blocks=True, lstrip_blocks=True)
        return template.render(**self.config)
