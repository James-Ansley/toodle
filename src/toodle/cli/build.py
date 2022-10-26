from pathlib import Path

from toodle import Quiz
from toodle.utils.logutils import log


@log(on_enter="Building: {0}", on_exit="Quiz written to: {1}\nDone!")
def build(root: Path, out: Path, /, include: list[str], exclude: list[str]):
    quiz = Quiz(root, glob=include, exclude=exclude)
    with open(out, "w") as f:
        f.write(quiz.to_xml())
