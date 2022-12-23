from pathlib import Path

from toodle.utils import logs
from toodle.core import Quiz
from toodle.core.serialization.xml.serializer import XMLSerializer


@logs.log_call(on_enter="Building {0}", on_exit="Writing to {1}\nDONE!")
def build(root: Path, out: Path, /, include: list[str], exclude: list[str]):
    quiz = Quiz(root, glob=include, exclude=exclude)
    with open(out, "w") as f:
        f.write(XMLSerializer.serialize_all(quiz))
