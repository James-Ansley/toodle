from typing import Any, Mapping

from toodle.utils.markup import resolve_to_html
from toodle.utils.files import resolve_directory, resolve_file
from .question import Question

_PRECHECK_OPTIONS = {
    "disabled": 0,
    "empty": 1,
    "examples": 2,
    "selected": 3,
    "all": 4,
}


class Coderunner(Question):
    @classmethod
    def suffix(cls):
        return "coderunner.toml"

    def _validate(self):
        pass

    def _serialize(self) -> Mapping[str, Any]:
        data = self.raw_data()
        root = self.root
        answer = resolve_file(root, data["answer"])
        return {
            **data,
            "prompt": resolve_to_html(root, data["prompt"]),
            "precheck": _PRECHECK_OPTIONS[data["precheck"].lower()],
            "answer": answer,
            "answerlines": answer.count("\n") + 1,
            "supportfiles": resolve_directory(
                root, data.get("supportfiles", [])
            ),
            "testcases": [
                case | {"example": int(case["example"])}
                for case in data["testcases"]
            ],
            "answerpreload": resolve_file(root, data["answerpreload"])
        }
