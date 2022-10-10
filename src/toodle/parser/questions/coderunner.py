import os
from base64 import b64encode
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from . import Question

__all__ = ["Coderunner"]

_PRECHECK_OPTIONS = {
    "disabled": 0,
    "empty": 1,
    "examples": 2,
    "selected": 3,
    "all": 4,
}


class Coderunner(Question):
    @property
    def template_name(self) -> str:
        return "coderunner.xml"

    @property
    def ans_path(self) -> Path:
        """
        The path to the Coderunner answer.py file

        :raises FileNotFoundError: if the answer file cannot be found
        """
        path = self.root / "answer.py"
        if not path.is_file():
            raise FileNotFoundError(f"answer.py file not found for {self.root}")
        return path

    @property
    def support_file_dir(self) -> Path:
        """The path to the support files – may or may not exist"""
        return self.root / "files"

    def answer(self):
        """The contents of answer.py"""
        with open(self.ans_path) as f:
            return f.read()

    def support_files(self) -> list[Mapping[str, str]]:
        """
        A list of support files as a mapping in the form:
        {"name": str, "data": str}
        """
        if not self.support_file_dir.exists():
            return []
        file_data = []
        for file in os.listdir(self.support_file_dir):
            path = self.support_file_dir / file
            with open(path, "rb") as f:
                data = b64encode(f.read())
            file_data.append({
                "name": path.name,
                "data": data.decode(),
            })
        return file_data

    def question_data(self) -> Mapping[str, Any]:
        data = super().question_data()
        answer = self.answer()
        return (
                data
                | {
                    "precheck": _parse_precheck(data["precheck"]),
                    "answer": answer,
                    "answerlines": answer.count("\n") + 1,
                    "supportfiles": self.support_files(),
                    "testcases": [
                        case | {"example": int(case["example"])}
                        for case in data["testcases"]
                    ]
                }
        )


def _parse_precheck(precheck_data: str) -> int:
    """
    Returns the precheck option as recognised by coderunner:
        "disabled": 0,
        "empty": 1,
        "examples": 2,
        "selected": 3,
        "all": 4,
    """
    return _PRECHECK_OPTIONS[precheck_data.lower()]
