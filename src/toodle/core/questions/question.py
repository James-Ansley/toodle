import abc
import tomllib
from pathlib import Path

from toodle.core.serialization import Serializable


class Question(Serializable, abc.ABC):
    def __init__(self, target: Path):
        self.root = target

    def raw_data(self):
        return tomllib.loads(self.root.read_text())

    @classmethod
    @abc.abstractmethod
    def suffix(cls):
        """The file suffix to recognise this question type by"""
