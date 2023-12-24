import typing


class RingElement[Compatible](typing.Protocol):
    type Compatible = Compatible | typing.Self

    @classmethod
    def one(cls) -> typing.Self:
        ...

    @classmethod
    def zero(cls) -> typing.Self:
        ...

    def __add__(self, other: Compatible) -> typing.Self:
        ...

    def __mul__(self, other: Compatible) -> typing.Self:
        ...


class FieldElement[Compatible](RingElement[Compatible], typing.Protocol):
    def __truediv__(self, other: Compatible) -> typing.Self:
        ...


class Zn:
    def __init__(self, n: int, value: int):
        pass
