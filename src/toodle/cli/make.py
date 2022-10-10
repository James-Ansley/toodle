from pathlib import Path

from toodle import Quiz


def make(root: Path, out: Path, include: list[str], exclude: list[str]):
    quiz = Quiz(root, glob=include, exclude=exclude)
    with open(out, "w") as f:
        f.write(quiz.to_xml())
