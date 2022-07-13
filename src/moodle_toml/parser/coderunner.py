import os
from base64 import b64encode
from functools import cached_property
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote

from bs4 import BeautifulSoup as Soup

from .question import Question

__all__ = ["Coderunner"]


class Coderunner(Question):
    _XML_NAME = "coderunner.xml"
    _ANSWER = "answer.py"
    _SUPPORT_FILES = "support_files"
    _CODERUNNER_INLINE_IMG_FORMAT = "@@PLUGINFILE@@/{}"

    _PRECHECK_OPTIONS = {
        "disabled": 0,
        "empty": 1,
        "examples": 2,
        "selected": 3,
        "all": 4,
    }

    @cached_property
    def answer(self) -> str:
        path = self.question_dir / self._ANSWER
        with open(path, "r") as f:
            return f.read()

    @cached_property
    def config(self) -> dict[str, Any]:
        config = super().config
        config["prompt"] = self._transform_images(config["prompt"])
        config["name"] = self.name
        config["precheck"] = self._PRECHECK_OPTIONS[config["precheck"].lower()]
        config["answer"] = self.answer
        config["answerlines"] = len(self.answer.splitlines()) + 1
        config["images"] = self.images
        config["supportfiles"] = self.support_files
        return config

    @cached_property
    def images(self):
        images = []
        for img in self.prompt.find_all("img"):
            path = self.question_dir / unquote(img["src"])
            with open(path, "rb") as f:
                data = b64encode(f.read())
            images.append({"name": path.name, "data": data.decode()})
        return images

    @cached_property
    def support_files(self):
        path = Path(self.question_dir / self._SUPPORT_FILES)
        if not path.exists():
            return []
        file_data = []
        files = [path / file for file in os.listdir(path)
                 if (path / file).is_file()]
        for file in files:
            with open(file, "rb") as f:
                data = b64encode(f.read())
            file_data.append({
                "name": file.name,
                "data": data.decode(),
            })
        return file_data

    def _transform_images(self, prompt: Soup):
        soup = Soup(str(prompt), "html.parser")
        for img in soup.find_all("img"):
            src = quote(Path(img["src"]).name)
            new_img = Soup("<img />", "html.parser").img
            new_img.attrs = {
                "alt": img["alt"],
                "src": self._CODERUNNER_INLINE_IMG_FORMAT.format(src),
                "role": "presentation",
                "class": "img-fluid"
            }
            img.replace_with(new_img)
        return soup
