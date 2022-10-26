from pathlib import Path

from toodle.qdata import QDATA_ROOT
from toodle.templates import Serializable, get_template

__all__ = ["Category"]


class Category(Serializable):
    def __init__(self, root: Path):
        self.root = root

    def to_xml(self):
        """Compiles question object to Moodle XML"""
        template_path = QDATA_ROOT / "category" / "template.xml"
        template = get_template(template_path)
        return template.render(category_name=self.root.name)
