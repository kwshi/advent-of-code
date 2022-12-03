# pyright: strict
import typing

import os
import io

import urllib.request
import urllib.parse

import html.parser
import textwrap


class SubmitResultParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.main = False
        self.paragraphs: list[str] = []
        self.paragraph: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        match tag:
            # main result text hierarchy: main > article > p
            case "main":
                self.main = True
            case "article":
                pass
            case "p":
                assert self.paragraph is None
                self.paragraph = []
            case "span":
                # special annotations: span.day-success for yellow highlight
                pass
            case "code":
                # special annotation: your guess
                pass
            case "a":
                # links: [Return to Day 7] (for example)
                pass

            case _:
                pass

    def handle_endtag(self, tag: str):
        match tag:
            case "p":
                assert self.paragraph is not None
                self.paragraphs.append(
                    textwrap.fill(" ".join(" ".join(self.paragraph).strip().split()))
                )
                self.paragraph = None
            case "main":
                assert self.main
                self.main = False
            case _:
                pass

    def handle_data(self, data: str):
        if self.paragraph is None:
            return
        self.paragraph.append(data)


def get_session() -> str:
    session = os.getenv("AOC_SESSION")
    assert (
        session is not None
    ), "AOC_SESSION not defined (obtain it from browser's cookies devtools on AoC website)"
    return session


def fetch_input(session: str, year: int, day: int) -> typing.TextIO:
    cache = os.getenv("AOC_INPUT_CACHE")
    assert cache is not None, "AOC_INPUT_CACHE not defined"

    year_path = os.path.join(cache, str(year))
    day_path = os.path.join(year_path, f"{day:02d}")

    if os.path.exists(day_path):
        return open(day_path, "r")

    os.makedirs(year_path, exist_ok=True)

    content = urllib.request.urlopen(
        urllib.request.Request(
            f"https://adventofcode.com/{year}/day/{day}/input",
            headers={"Cookie": f"session={session}"},
        )
    ).read()

    with open(day_path, "wb") as f:
        f.write(content)

    return io.StringIO(content.decode())


def submit_answer(session: str, year: int, day: int, part: int, answer: str):
    parser = SubmitResultParser()
    parser.feed(
        urllib.request.urlopen(
            urllib.request.Request(
                f"https://adventofcode.com/{year}/day/{day}/answer",
                headers={"Cookie": f"session={session}"},
                data=urllib.parse.urlencode(
                    {"level": str(part), "answer": answer}
                ).encode(),
            )
        )
        .read()
        .decode()
    )
    print("\n\n".join(parser.paragraphs))
