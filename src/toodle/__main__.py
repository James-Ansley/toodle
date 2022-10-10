from pathlib import Path

import typer
from typer import Argument, Option

from toodle import cli

app = typer.Typer(
    add_completion=False,
)


@app.command("make")
def make(
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
            help="Glob patterns to select "
                 "questions/categories in root",
        ),
        exclude: list[str] = Option(
            [],
            help="Glob patterns to exclude "
                 "questions/categories in root"
        )
):
    cli.make(root, out, include, exclude)


app()
