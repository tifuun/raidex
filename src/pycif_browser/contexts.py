from typing import List, Set
from dataclasses import dataclass, field


@dataclass
class CTXOption(object):
    """
    jinja2 context for a componenent option.
    """

    name: str
    default_value: str
    description: str
    shadow: bool


@dataclass
class CTXLayer(object):
    """
    jinja2 context for a componenent layer.
    """

    name: str
    index: int
    image_string: str  # the entire svg image as a string
    image_path: str | None = None  # Path to image. Unused.

@dataclass
class CTXInterface(object):
    """
    jinja2 context for a compo interface.
    """

    name: str


@dataclass
class CTXMark(object):
    """
    jinja2 context for a mark.
    """

    name: str


@dataclass
class CTXMethod(object):
    """
    jinja2 context for a method.
    """

    name: str
    short_description: str
    long_description: str


@dataclass
class CTXCompo(object):
    """
    jinja2 context for a compo.
    """

    name: str
    fancy_name: str
    module_name: str
    package_name: str
    author: str
    description: str
    options: List[CTXOption]
    layers: List[CTXLayer]
    interfaces: List[CTXInterface]
    marks: List[CTXMark]
    methods: List[CTXMethod]
    tags: List[str]
    #preview_image: str

@dataclass
class CTXBrowser(object):
    """
    jinja2 context for the entire browser page
    """
    all_tags: Set[str] = field(
        default_factory=lambda: set()
        )

    all_packages: List[str] = field(
        default_factory=lambda: set(),
        )

    compos: List[CTXCompo] = field(
        default_factory=lambda: [],
        )

