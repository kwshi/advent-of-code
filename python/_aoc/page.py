# pyright: strict

import dataclasses

import typing

A = typing.TypeVar("A")


@dataclasses.dataclass
class Text:
    text: str
    em: bool


@dataclasses.dataclass
class Code:
    content: list[Text]


@dataclasses.dataclass
class Link:
    href: str
    content: list[Text]


Node = Text | Code | Link


@dataclasses.dataclass
class Header:
    content: list[Node]


@dataclasses.dataclass
class CodeBlock:
    content: list[Text]


@dataclasses.dataclass
class List:
    items: list[list[Node]]


@dataclasses.dataclass
class Paragraph:
    content: list[Node]


Block = Header | Paragraph | List | CodeBlock

Article = list[Block]
