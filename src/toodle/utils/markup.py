from collections.abc import Mapping
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt

from .images import link_images

_formats = {".md": "markdown", ".html": "html"}


def resolve_to_html(target: Path, markup: Mapping[str, Any]):
    if "file" in markup:
        markup = to_markup(target, markup)
    return to_html(target, markup)


def to_markup(target: Path, file: Mapping[str, Any]):
    path = (target / ".." / file["file"]).resolve()
    return {
        **file,
        "format": _formats[path.suffix],
        "text": path.read_text(),
    }


def to_html(target: Path, data: Mapping[str, Any]):
    if data["format"] == "markdown":
        data |= {
            "format": "html",
            "text": MarkdownIt("gfm-like").render(data["text"]),
        }
    data = link_images(target, data)
    return data
