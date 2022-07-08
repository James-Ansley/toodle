import os
from pathlib import Path

import tomli
from jinja2 import Template

from . import coderunner, category, shortanswer
from .. import TEMPLATE_DIR

__all__ = ["to_xml"]


def _parse_question(path: Path):
    with open(path / "config.toml", "rb") as f:
        qtype = tomli.load(f)["qtype"]
    if qtype == "coderunner":
        return coderunner.parse(path)
    if qtype == "shortanswer":
        return shortanswer.parse(path)


def _parse_category(path, root):
    root_parts = root.parts
    return category.parse(path.parts[len(root_parts):])


def _walk_questions(root: Path):
    for dirpath, _, filenames in os.walk(root):
        path = Path(dirpath)
        if path == root:
            continue
        if "config.toml" in filenames:
            yield _parse_question(path)
        else:
            yield _parse_category(path, root)


def to_xml(questions_path: Path):
    with open(TEMPLATE_DIR / "quiz.xml", "r") as f:
        template = Template(f.read(), trim_blocks=True, lstrip_blocks=True)
    return template.render(data=_walk_questions(questions_path))
