from collections.abc import Mapping
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup as Soup

from toodle.utils.files import to_bs4_file

_IMAGE_SRC = "data:image/{type};base64,{data}"


def link_images(target: Path, data: Mapping[str, Any]):
    soup = Soup(data["text"], "html.parser")
    images = []
    for img in soup.find_all("img"):
        path = target.parent / img["src"]
        images.append(to_bs4_file(path))
        img.attrs |= {"src": f"@@PLUGINFILE@@/{path.name}"}
    return {
        **data,
        "format": "html",
        "text": str(soup),
        "images": images,
    }
