from functools import cached_property
from typing import Any

from .question import Question

__all__ = ["Category"]


class Category(Question):
    _XML_NAME = "category.xml"

    def __init__(self, *args, root, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root

    @cached_property
    def config(self) -> dict[str, Any]:
        root_parts = self.root.parts
        parts = self.question_dir.parts[len(root_parts):]
        return {"category_name": "/".join(parts)}

    @cached_property
    def prompt(self):
        return None
