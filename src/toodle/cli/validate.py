from toodle.core import Quiz
from toodle.utils import logs


@logs.log_call(on_enter="Validating questions in {0}", on_exit="All OK!")
def validate(root, /, include: list[str], exclude: list[str]):
    quiz = Quiz(root, glob=include, exclude=exclude)
    for question in quiz:
        question.validate()
