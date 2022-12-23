from typing import Any, Mapping

from toodle.core.questions.question import Question
from toodle.utils.markup import resolve_to_html


class Category(Question):
    @classmethod
    def suffix(cls):
        return "category.toml"

    def _validate(self):
        pass

    def _serialize(self) -> Mapping[str, Any]:
        data = self.raw_data()
        if "info" in data:
            data = data | {"info": resolve_to_html(self.root, data["info"])}
        return {
            **data,
            "category": data.get("category", self.root.parent.as_posix()),
        }
