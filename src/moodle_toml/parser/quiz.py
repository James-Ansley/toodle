import os
from functools import cached_property
from pathlib import Path
from typing import Any

from .utils import question_to_xml
from .category import Category
from .question import Question


class Quiz(Question):
    _XML_NAME = "quiz.xml"

    @cached_property
    def config(self) -> dict[str, Any]:
        return {"data": self._walk_questions()}

    @cached_property
    def prompt(self):
        return None

    def _walk_questions(self):
        for dirpath, dirnames, filenames in os.walk(self.question_dir):
            path = Path(dirpath)
            if path == self.question_dir:
                continue
            if Question.QUESTION_CONFIG in filenames:
                dirnames[:] = []
                yield question_to_xml(path)
            else:
                yield Category(path, root=self.question_dir).as_xml()
