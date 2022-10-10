import os
from collections.abc import Generator, Iterable
from fnmatch import fnmatch
from pathlib import Path

import tomli

from .category import Category
from .questions import *
from toodle.templates import TEMPLATE_ENVIRONMENT, Serializable


__all__ = ["Quiz"]


class Quiz(Serializable):
    """
    A quiz transpiler.

    For some unknown reason, Moodle "quizzes" are not the same as "quizzes"
    used in Moodle XML. Here, a quiz is a container for questions and
    categories used in the XML – NOT a "quiz" activity within a course.
    """

    def __init__(
            self,
            root: Path,
            *,
            glob: Iterable[str] = ("*",),
            exclude: Iterable[str] = ("",),
    ):
        """
        :param root: the root directory questions will be parsed from
        :param glob: optional glob pattern that matches
        """
        self.root = root
        self.glob = list(glob)
        self.exclude = list(exclude)

    @property
    def template_name(self) -> str:
        return "quiz.xml"

    def to_xml(self):
        template = TEMPLATE_ENVIRONMENT.get_template(self.template_name)
        questions = self._walk_questions()
        return template.render(data=(q.to_xml() for q in questions))

    def _walk_questions(self) -> Generator[Serializable, None, None]:
        for dirpath, dirnames, filenames in os.walk(self.root):
            path = Path(dirpath)
            is_match = any(fnmatch(path.as_posix(), g) for g in self.glob)
            is_excluded = any(fnmatch(path.as_posix(), g) for g in self.exclude)
            if path == self.root or is_excluded or not is_match:
                continue
            if "config.toml" in filenames:
                dirnames[:] = []
                yield _make_question(path)
            else:
                yield Category(path)


def _make_question(root: Path) -> Question:
    """Question factory – determines type from config.toml. Config is cached"""
    conf_path = root / Question.CONFIG_FILENAME
    with open(conf_path, "rb") as f:
        data = tomli.load(f)

    qtype = data["qtype"]
    match qtype:
        case "shortanswer":
            return ShortAnswer(root, config_cache=data)
        case "coderunner":
            return Coderunner(root, config_cache=data)
        case _:
            raise ValueError(f"Unrecognised qtype, '{qtype}', in {conf_path}")
