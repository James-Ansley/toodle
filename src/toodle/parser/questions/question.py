import abc
from base64 import b64encode
from collections.abc import Generator, Mapping
from pathlib import Path
from typing import Any
from urllib.parse import quote

import tomli
from bs4 import BeautifulSoup as Soup
from markdown import markdown

from toodle.templates import TEMPLATE_ENVIRONMENT, Serializable

__all__ = ["Question"]


_IMG_SRC_FMT = "@@PLUGINFILE@@/{}"


class Question(Serializable, abc.ABC):
    CONFIG_FILENAME = "config.toml"

    def __init__(self, root: Path, config_cache: Mapping = None):
        """
        A generic question representation

        :param root: the question root directory that minimally contains the
            question config and prompt file.
        """
        self.root = root
        self._config_cache = config_cache

    @property
    def conf_path(self) -> Path:
        """
        The path to config.toml within the root question directory

        :raises FileNotFoundError: if a config.toml file does not exist
        """
        path = self.root / Question.CONFIG_FILENAME
        if not path.is_file():
            raise FileNotFoundError(f"Cannot find config.toml in {self.root}")
        return path

    @property
    def prompt_path(self) -> Path:
        """
        The path to the prompt.md or prompt.html file

        :raises FileNotFoundError: if a prompt file does not exist
        """
        md = self.root / "prompt.md"
        if md.exists():
            return md
        html = self.root / "prompt.html"
        if html.exists():
            return html
        raise FileNotFoundError(f"Cannot find prompt file in {self.root}")

    @property
    def img_dir(self) -> Path:
        """The path to the images directory – may or may not exist"""
        return self.root / "images"

    @property
    def img_paths(self) -> Generator[Path, None, None]:
        """
        Yields paths to all files contained within the images directory.
        Returns an empty generator in the case no such directory exists.
        """
        yield from self.img_dir.glob("?*.?*")

    def question_data(self) -> Mapping[str, Any]:
        """
        A mapping of data that will be passed to the template params.

        Default behaviour returns all data from config.toml, the question name
        (root directory name for question), the prompt as an HTML string,
        and a list of images associated with the question prompt.
        """
        return self.config() | {
            "name": self.root.name,
            "prompt": self.prompt(),
            "images": self.images(),
        }

    def config(self) -> Mapping[str, Any]:
        """
        A mapping of config names to values
        uses cached config if available
        """
        if self._config_cache is None:
            with open(self.conf_path, "rb") as f:
                self._config_cache = tomli.load(f)
        return self._config_cache

    def prompt(self) -> str:
        """The prompt as an HTML string"""
        with open(self.prompt_path, "r") as f:
            prompt = f.read()
        if self.prompt_path.suffix == ".md":
            prompt = markdown(prompt)
        prompt = self._link_images(prompt)
        return prompt

    def images(self) -> list[Mapping[str, str]]:
        """
        Returns a list of images mapping image names and base 64 encoded
        image strings of the form {"name": ..., "data": ...}
        """
        images = []
        for image in self.img_paths:
            with open(image, "rb") as f:
                data = b64encode(f.read())
            images.append({"name": image.name, "data": data.decode()})
        return images

    def to_xml(self):
        template = TEMPLATE_ENVIRONMENT.get_template(self.template_name)
        return template.render(
            **self.question_data(), trim_blocks=True, lstrip_blocks=True
        )

    def _link_images(self, prompt: str) -> str:
        image_files = {img.name for img in self.img_paths}
        soup = Soup(prompt, "html.parser")
        for img in soup.find_all("img"):
            src = quote(Path(img["src"]).name)
            if src not in image_files:
                raise ValueError(
                    "Prompt contains image not present in images: "
                    f"{src} in {self.root}"
                )
            img.attrs |= {
                "src": _IMG_SRC_FMT.format(src),
                "role": "presentation",
                "class": "img-fluid",
            }
        return str(soup)
