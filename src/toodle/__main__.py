from pathlib import Path

import typer
from typer import Argument, Option

from toodle import cli
from toodle.utils import logs

app = typer.Typer(
    add_completion=False,
)

logs.attach()


@app.command(
    "build",
    help="Transpiles questions to Moodle XML",
)
def build(
        root: Path = Argument(
            ...,
            help="The root directory of questions to be transpiled"
        ),
        out: Path = Option(
            ...,
            "--out", "-o",
            help="The path the Moodle XML will be written to",
        ),
        include: list[str] = Option(
            ["*"],
            help="Glob patterns to select questions/categories in root",
        ),
        exclude: list[str] = Option(
            [],
            help="Glob patterns to exclude questions/categories in root"
        )
):
    cli.build(root, out, include, exclude)


@app.command(
    "validate",
    help="Validates all questions",
)
def build(
        root: Path = Argument(
            ...,
            help="The root directory of questions to be validated"
        ),
        include: list[str] = Option(
            ["*"],
            help="Glob patterns to select questions/categories in root",
        ),
        exclude: list[str] = Option(
            [],
            help="Glob patterns to exclude questions/categories in root"
        )
):
    cli.validate(root, include, exclude)


app()
