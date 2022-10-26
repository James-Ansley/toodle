import abc
from base64 import b64encode
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any
from urllib.parse import quote

import tomli
from bs4 import BeautifulSoup as Soup
from markdown import markdown

from toodle.qdata import QDATA_ROOT
from toodle.templates import Serializable, get_template

__all__ = ["Question"]

_IMG_SRC_FMT = "@@PLUGINFILE@@/{}"


class Question(Serializable, abc.ABC):
    CONFIG_FILENAME = "config.toml"

    def __init__(self, root: Path, config: Mapping = None):
        """
        A generic question representation

        :param root: the question root directory that minimally contains the
            question config and prompt file.
        :param config: An optional config option – is intended to be used as a
            cache to prevent rereading the config file.
        """
        self._root = root
        self._config = config

    @classmethod
    def qtype_name(cls):
        """
        The name of this question type. By default, the lowercase classname.
        Used for templates and schema validation
        """
        return cls.__name__.lower()

    @classmethod
    def qdata_dir(cls) -> Path:
        """The path to the question data directory"""
        return QDATA_ROOT / cls.qtype_name()

    @property
    def name(self):
        """The name of the question instance"""
        return self._root.name

    @property
    def conf_path(self) -> Path:
        """
        The path to config.toml within the root question directory

        :raises FileNotFoundError: if a config.toml file does not exist
        """
        path = self._root / Question.CONFIG_FILENAME
        if not path.is_file():
            raise FileNotFoundError(f"Cannot find config.toml in {self._root}")
        return path

    @property
    def prompt_path(self) -> Path:
        """
        The path to the prompt.md or prompt.html file

        :raises FileNotFoundError: if a prompt file does not exist
        """
        md = self._root / "prompt.md"
        if md.exists():
            return md
        html = self._root / "prompt.html"
        if html.exists():
            return html
        raise FileNotFoundError(f"Cannot find prompt file in {self._root}")

    @property
    def img_dir(self) -> Path:
        """The path to the images directory – may or may not exist"""
        return self._root / "images"

    @property
    def img_paths(self) -> Iterator[Path]:
        """
        Yields paths to all files contained within the images directory.
        Returns an empty generator in the case no such directory exists.
        """
        yield from self.img_dir.glob("?*.?*")

    @abc.abstractmethod
    def _question_data(self) -> Mapping[str, Any]:
        """
        Returns question type-specific data.
        Values returned in this mapping will override those defined by default
        in the public question_data method
        """

    def question_data(self) -> Mapping[str, Any]:
        """
        A mapping of data that will be passed to the template params.

        Default behaviour returns all data from config.toml, the question name
        (root directory name for question), the prompt as an HTML string,
        and a list of images associated with the question prompt.
        """
        return (
                self.config()
                | {
                    "name": self.name,
                    "prompt": self.prompt(),
                    "images": self.images(),
                }
                | self._question_data()
        )

    def config(self) -> Mapping[str, Any]:
        """
        A mapping of config names to values. Uses cached config if available
        """
        if self._config is None:
            with open(self.conf_path, "rb") as f:
                self._config = tomli.load(f)
        return self._config

    def prompt(self) -> str:
        """The prompt as an HTML string"""
        with open(self.prompt_path, "r") as f:
            prompt = f.read()
        if self.prompt_path.suffix == ".md":
            prompt = markdown(prompt)
        prompt = self._link_images(prompt)
        return prompt

    def images(self) -> Iterator[Mapping[str, str]]:
        """
        Returns a list of images mapping image names and base 64 encoded
        image data of the form {"name": ..., "data": ...}
        """
        for image in self.img_paths:
            with open(image, "rb") as f:
                data = b64encode(f.read())
            yield {"name": image.name, "data": data.decode()}

    def to_xml(self):
        template_path = type(self).qdata_dir() / "template.xml"
        template = get_template(template_path)
        return template.render(**self.question_data())

    def _link_images(self, prompt: str) -> str:
        """
        Redirects image src links in the prompt HTML to images from the
        "images" directory to instead be marked as plugin files.
        """
        image_files = {img.name for img in self.img_paths}
        soup = Soup(prompt, "html.parser")
        for img in soup.find_all("img"):
            src = quote(Path(img["src"]).name)
            if src not in image_files:
                raise ValueError(
                    "Prompt references image not present in images dir: "
                    f"{src} in {self._root}"
                )
            img.attrs |= {
                "src": _IMG_SRC_FMT.format(src),
                "role": "presentation",
                "class": "img-fluid",
            }
        return str(soup)
