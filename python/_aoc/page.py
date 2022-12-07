# pyright: strict

import dataclasses

import typing

A = typing.TypeVar("A")


@dataclasses.dataclass
class Text:
    text: str
    em: bool


@dataclasses.dataclass
class Code(typing.Generic[A]):
    content: list[A]


@dataclasses.dataclass
class Link(typing.Generic[A]):
    href: str
    content: list[A]


Node = Text | Code[Text | Link[Text]] | Link[Text | Code[Text]]


@dataclasses.dataclass
class Header:
    content: list[Node]


@dataclasses.dataclass
class CodeBlock:
    content: list[Text | Link[Text]]


@dataclasses.dataclass
class List:
    items: list[list[Node]]


@dataclasses.dataclass
class Paragraph:
    content: list[Node]


Block = Header | Paragraph | List | CodeBlock

Article = list[Block]
