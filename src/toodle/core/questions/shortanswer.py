from typing import Any, Mapping

from .question import Question
from toodle.utils.markup import resolve_to_html


class ShortAnswer(Question):
    @classmethod
    def suffix(cls):
        return "shortanswer.toml"

    def _serialize(self) -> Mapping[str, Any]:
        data = self.raw_data()
        root = self.root
        answers = []
        for answer in data["answers"]:
            if "feedback" in answer:
                answer["feedback"] = resolve_to_html(root, answer["feedback"])
            answers.append(answer)
        return {
            **data,
            "prompt": resolve_to_html(root, data["prompt"]),
            "casesensitivity": int(data['casesensitivity']),
            "answers": answers,
        }

    def _validate(self):
        pass
