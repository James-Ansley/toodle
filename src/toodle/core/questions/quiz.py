import os
from collections.abc import Iterable, Iterator
from fnmatch import fnmatch
from pathlib import Path

from toodle.utils import logs
from toodle.core.questions import Category, Question


class Quiz(Iterable[Question]):
    def __init__(
            self,
            root: Path,
            *,
            glob: Iterable[str] = ("*",),
            exclude: Iterable[str] = tuple(),
    ):
        self.root = root
        self.glob = list(glob)
        self.exclude = list(exclude)

    def should_ignore(self, path: Path):
        is_match = any(fnmatch(path.as_posix(), g) for g in self.glob)
        is_excluded = any(fnmatch(path.as_posix(), g) for g in self.exclude)
        return path == self.root or is_excluded or not is_match

    def __iter__(self) -> Iterator[Question]:
        for dirpath, dirnames, filenames in os.walk(self.root):
            root = Path(dirpath)
            files = [root / fname for fname in filenames
                     if not self.should_ignore(root / fname)]
            yield from _match_categories(files, self.root)
            yield from _match_questions(files, self.root)


def _match_categories(files: list[Path], root: Path):
    for file in files:
        if file.name.endswith(Category.suffix()):
            logs.log_tree(f"Category: {file}", root, file)
            yield Category(file)


def _match_questions(files: list[Path], root: Path):
    q_types = [QType for QType in Question.__subclasses__()
               if QType is not Category]
    for file in files:
        for QType in q_types:
            if file.name.endswith(QType.suffix()):
                logs.log_tree(f"Question: {file}", root, file)
                yield QType(file)
