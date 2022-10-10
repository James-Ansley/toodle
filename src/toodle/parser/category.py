from pathlib import Path

from toodle.templates import TEMPLATE_ENVIRONMENT, Serializable


__all__ = ["Category"]


class Category(Serializable):
    def __init__(self, root: Path):
        self.root = root

    @property
    def template_name(self) -> str:
        return "category.xml"

    def to_xml(self):
        """Compiles question object to Moodle XML"""
        template = TEMPLATE_ENVIRONMENT.get_template(self.template_name)
        return template.render(
            category_name=self.root.name, trim_blocks=True, lstrip_blocks=True
        )
