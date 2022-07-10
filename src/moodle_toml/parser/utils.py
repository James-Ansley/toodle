from pathlib import Path

import tomli

from .coderunner import Coderunner
from .question import Question
from .shortanswer import ShortAnswer


def question_to_xml(path: Path):
    with open(path / Question.QUESTION_CONFIG, "rb") as f:
        qtype = tomli.load(f)["qtype"]
    if qtype == "coderunner":
        return Coderunner(path).as_xml()
    if qtype == "shortanswer":
        return ShortAnswer(path).as_xml()
