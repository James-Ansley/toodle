from pathlib import Path

import typer
from typer import Argument, Option

from toodle import cli
from toodle.utils import logutils

app = typer.Typer(
    add_completion=False,
)

logutils.attach()


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
    "new",
    help="Generates a blank question template in the current working directory",
)
def new(
        qtype: str = Argument(
            ...,
            help="The question type to generate",
        ),
        name: str = Argument(
            ...,
            help="The name of the question to generate",
        ),
):
    cli.new(qtype, name)


app()
