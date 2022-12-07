# pyright: strict

import html.parser
import dataclasses
import enum

from . import page


class StateMode(enum.Enum):
    BEFORE_MAIN = "BEFORE_MAIN"
    IN_MAIN = "IN_MAIN"
    IN_ARTICLE = "IN_ARTICLE"
    IN_HEADER = "IN_HEADER"
    IN_PARAGRAPH = "IN_PARAGRAPH"
    IN_LIST = "IN_LIST"
    IN_LIST_ITEM = "IN_LIST_ITEM"
    IN_PRE = "IN_PRE"
    AFTER_MAIN = "AFTER_MAIN"


class ParagraphType(enum.Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADER = "HEADER"


@dataclasses.dataclass
class StateRoot:
    articles: list[page.Article] | None

    def start(self, tag: str, _: dict[str, str | None]):
        if tag == "main":
            return StateMain(root=self, open_tags=[], articles=[])

    def data(self, _: str):
        pass

    def end(self, _: str):
        return self


@dataclasses.dataclass
class StateMain:
    root: StateRoot
    open_tags: list[str]
    articles: list[page.Article]

    def start(self, tag: str, _: dict[str, str | None]):
        depth = self.push_tag(tag)
        if tag == "article":
            return StateArticle(main=self, tag_depth=depth, blocks=[])

    def data(self, _: str):
        pass

    def end(self, tag: str):
        if tag != "main" or self.open_tags:
            return
        self.root.articles = self.articles
        return self.root

    def push_tag(self, tag: str) -> int:
        depth = len(self.open_tags)
        self.open_tags.append(tag)
        return depth

    def pop_tag(self, tag: str) -> int:
        pop = self.open_tags.pop()
        assert tag == pop, f"start/end tag mismatch: start is {pop!r}, end is {tag!r}"
        return len(self.open_tags)


@dataclasses.dataclass
class StateArticle:
    main: StateMain
    tag_depth: int
    blocks: list[page.Block]

    def _start_paragraph(self, type: ParagraphType, depth: int):
        return StateParagraph(
            type=type, article=self, tag_depth=depth, text=TextStateRoot()
        )

    def start(self, tag: str, _: dict[str, str | None]):
        depth = self.main.push_tag(tag)
        match tag:
            case "h1" | "h2" | "h3" | "h4" | "h5" | "h6":
                return self._start_paragraph(ParagraphType.HEADER, depth)

            case "p":
                return self._start_paragraph(ParagraphType.PARAGRAPH, depth)

            case "ul" | "ol":
                return StateList(article=self, tag_depth=depth, items=[])

            case "pre":
                return StateCodeBlock(
                    article=self, tag_depth=depth, nodes=[], em_tag_depth=None
                )

            case _:
                pass

    def data(self, _: str):
        pass

    def end(self, tag: str):
        depth = self.main.pop_tag(tag)
        if depth != self.tag_depth:
            assert depth > self.tag_depth
            return
        self.main.articles.append(self.blocks)
        return self.main


@dataclasses.dataclass
class StateList:
    article: StateArticle
    tag_depth: int
    items: list[list[page.Node]]

    def add_child(self, child: list[page.Node]):
        self.items.append(child)

    def start(self, tag: str, _: dict[str, str | None]):
        depth = self.article.main.push_tag(tag)
        if tag == "li":
            return StateListItem(parent=self, tag_depth=depth, text=TextStateRoot())

    def data(self, _: str):
        pass

    def end(self, tag: str):
        depth = self.article.main.pop_tag(tag)
        if depth != self.tag_depth:
            assert depth > self.tag_depth
            return
        self.article.blocks.append(page.List(self.items))
        return self.article


@dataclasses.dataclass
class TextStateRoot:
    nodes: list[page.Node] = dataclasses.field(default_factory=list)
    em_tag_depth: int | None = dataclasses.field(default=None)

    def start(self, tag: str, depth: int):
        match tag:
            case "em":
                self.start_em(depth)

            case "code":
                return TextStateCode(parent=self, tag_depth=depth, nodes=[])

            case "a":
                return TextStateLink(
                    parent=self, tag_depth=depth, href="TODO TODO TODO", nodes=[]
                )

            case _:
                pass

    def data(self, _: str):
        pass

    def start_em(self, depth: int):
        if self.em_tag_depth is None:
            self.em_tag_depth = depth

    def end_em(self, depth: int):
        if depth == self.em_tag_depth:
            self.em_tag_depth = None

    def end(self, tag: str, depth: int) -> None:
        match tag:
            case "em":
                if depth == self.em_tag_depth:
                    self.em_tag_depth = None

            case _:
                pass


@dataclasses.dataclass
class TextStateCode:
    parent: TextStateRoot
    tag_depth: int
    nodes: list[page.Text | page.Link[page.Text]]

    def start(self, tag: str, depth: int):
        match tag:
            case "em":
                self.parent.start_em(depth)
            case "a":
                return TextStateCodeLink(
                    parent=self, href="TODO", tag_depth=depth, text=[]
                )
            case _:
                pass

    def data(self, _: str):
        pass

    def end(self, tag: str, depth: int):
        match tag:
            case "em":
                self.parent.end_em(depth)
            case "code":
                self.parent.nodes.append(page.Code(self.nodes))
                return self.parent
            case _:
                pass


@dataclasses.dataclass
class TextStateCodeLink:
    parent: TextStateCode
    href: str
    tag_depth: int
    text: list[page.Text]

    def start(self, tag: str, depth: int):
        match tag:
            case "em":
                self.parent.parent.start_em(depth)
            case _:
                pass

    def data(self, _: str):
        pass

    def end(self, tag: str, depth: int):
        match tag:
            case "em":
                self.parent.parent.end_em(depth)
            case "a":
                self.parent.nodes.append(page.Link(self.href, self.text))
                return self.parent
            case _:
                pass


@dataclasses.dataclass
class TextStateLink:
    parent: TextStateRoot
    tag_depth: int
    href: str
    nodes: list[page.Text | page.Code[page.Text]]

    def start(self, tag: str, depth: int):
        match tag:
            case "em":
                self.parent.start_em(depth)
            case _:
                pass

    def data(self, _: str):
        pass

    def end(self, tag: str, depth: int):
        match tag:
            case "em":
                self.parent.end_em(depth)
            case "a":
                self.parent.nodes.append(page.Link(self.href, self.nodes))
                return self.parent
            case _:
                pass


@dataclasses.dataclass
class TextStateLinkCode:
    parent: TextStateLink
    tag_depth: int
    nodes: list[page.Text]

    def start(self, tag: str, depth: int):
        match tag:
            case "em":
                self.parent.parent.start_em(depth)
            case _:
                pass

    def data(self, _: str):
        pass

    def end(self, tag: str, depth: int):
        match tag:
            case "em":
                self.parent.parent.end_em(depth)
            case "a":
                self.parent.nodes.append(page.Code(self.nodes))
                return self.parent
            case _:
                pass


TextState = (
    TextStateRoot
    | TextStateCode
    | TextStateLink
    | TextStateCodeLink
    | TextStateLinkCode
)


@dataclasses.dataclass
class StateParagraph:
    type: ParagraphType
    article: StateArticle
    tag_depth: int
    text: TextState

    def start(self, tag: str, _: dict[str, str | None]):
        depth = self.article.main.push_tag(tag)
        self.text = self.text.start(tag, depth) or self.text

    def data(self, _: str):
        pass

    def end(self, tag: str):
        depth = self.article.main.pop_tag(tag)
        self.text = self.text.end(tag, depth) or self.text
        if depth != self.tag_depth:
            assert depth > self.tag_depth
            return
        assert isinstance(self.text, TextStateRoot)
        self.article.blocks.append(page.Paragraph(self.text.nodes))
        return self.article


@dataclasses.dataclass
class StateListItem:
    tag_depth: int
    text: TextState
    parent: StateList

    def start(self, tag: str, _: dict[str, str | None]):
        depth = self.parent.article.main.push_tag(tag)
        self.text = self.text.start(tag, depth) or self.text

    def data(self, _: str):
        pass

    def end(self, tag: str):
        depth = self.parent.article.main.pop_tag(tag)
        self.text = self.text.end(tag, depth) or self.text
        if depth != self.tag_depth:
            assert depth > self.tag_depth
            return
        assert isinstance(self.text, TextStateRoot)
        self.parent.items.append(self.text.nodes)
        return self.parent


@dataclasses.dataclass
class StateCodeBlock:
    article: StateArticle
    tag_depth: int
    nodes: list[page.Text | page.Link[page.Text]]
    em_tag_depth: int | None

    def start(self, tag: str, _: dict[str, str | None]):
        depth = self.article.main.push_tag(tag)
        match tag:
            case "em":
                if self.em_tag_depth is None:
                    self.em_tag_depth = depth

            case _:
                pass

    def data(self, _: str):
        pass

    def end(self, tag: str):
        depth = self.article.main.pop_tag(tag)
        if depth != self.tag_depth:
            assert depth > self.tag_depth
            return
        self.article.blocks.append(page.CodeBlock(self.nodes))
        return self.article


State = (
    StateRoot
    | StateMain
    | StateArticle
    | StateParagraph
    | StateCodeBlock
    | StateList
    | StateListItem
)


class PageParser(html.parser.HTMLParser):
    def __init__(self):
        self.state: State = StateRoot(articles=None)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        self.state = self.state.start(tag, dict(attrs)) or self.state

    def handle_endtag(self, tag: str):
        self.state = self.state.end(tag) or self.state

    def handle_data(self, data: str):
        self.state.data(data)
