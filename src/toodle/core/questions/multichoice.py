from typing import Any, Mapping

from toodle.utils.markup import resolve_to_html
from .question import Question


class MultiChoice(Question):
    @classmethod
    def suffix(cls):
        return "multichoice.toml"

    def _validate(self):
        pass

    def _serialize(self) -> Mapping[str, Any]:
        data = self.raw_data()
        root = self.root
        answers = []
        for answer in data["answers"]:
            answer = resolve_to_html(root, answer)
            if "feedback" in answer:
                answer["feedback"] = resolve_to_html(root, answer["feedback"])
            answers.append(answer)
        return {
            **data,
            "prompt": resolve_to_html(root, data["prompt"]),
            "answers": answers,
        }
