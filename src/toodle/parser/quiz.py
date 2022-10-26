import os
from collections.abc import Iterable, Iterator
from fnmatch import fnmatch
from pathlib import Path

import tomli

from toodle.templates import Serializable, get_template
from .category import Category
from .questions import *
from toodle.utils.logutils import log, log_tree

__all__ = ["Quiz"]

from ..qdata import QDATA_ROOT


class Quiz(Serializable):
    def __init__(
            self,
            root: Path,
            *,
            glob: Iterable[str] = ("*",),
            exclude: Iterable[str] = tuple(),
    ):
        """
        A quiz transpiler.

        For some unknown reason, Moodle "quizzes" are not the same as "quizzes"
        used in Moodle XML. Here, a quiz is a container for questions and
        categories used in the XML – NOT a "quiz" activity within a course.

        :param root: the root directory questions will be parsed from
        :param glob: optional glob patterns to select paths/files to bundle
        :param exclude: optional glob patterns to exclude paths/files
        """
        self.root = root
        self.glob = list(glob)
        self.exclude = list(exclude)

    def to_xml(self):
        template_path = QDATA_ROOT / "quiz" / "template.xml"
        template = get_template(template_path)
        questions = self._walk_questions()
        return template.render(data=(q.to_xml() for q in questions))

    @log(on_enter="Found the Following:")
    def _walk_questions(self) -> Iterator[Serializable]:
        for dirpath, dirnames, filenames in os.walk(self.root):
            path = Path(dirpath)
            is_match = any(fnmatch(path.as_posix(), g) for g in self.glob)
            is_excluded = any(fnmatch(path.as_posix(), g) for g in self.exclude)
            if path == self.root or is_excluded or not is_match:
                continue
            if Question.CONFIG_FILENAME in filenames:
                dirnames[:] = []
                log_tree(f"Question: {path.name}", self.root, path)
                yield _make_question(path)
            else:
                log_tree(f"Category: {path.name}:", self.root, path)
                yield Category(path)


def _make_question(root: Path) -> Question:
    """Question factory – determines type from config.toml. Config is cached"""
    conf_path = root / Question.CONFIG_FILENAME
    with open(conf_path, "rb") as f:
        data = tomli.load(f)

    qtype = data.get("qtype", None)
    # TODO – Dynamic question registration
    match qtype:
        case "shortanswer":
            return ShortAnswer(root, config=data)
        case "multichoice":
            return MultiChoice(root, config=data)
        case "coderunner":
            return Coderunner(root, config=data)
        case None:
            raise ValueError("Invalid question configuration. "
                             f"{conf_path} has no qtype field")
        case _:
            raise ValueError(f"Unrecognised qtype, '{qtype}', in {conf_path}")
