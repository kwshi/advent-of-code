# pyright: strict
import typing

import os
import io

import urllib.request
import urllib.parse

import html.parser
import textwrap

BASE_URL = "https://adventofcode.com"
USER_AGENT = "github.com/kwshi/advent-of-code by shi.kye@gmail.com / python"


class Client:
    def __init__(self, session: str, input_cache: str):
        self._session = session
        self._cache = input_cache

        self._headers = {"Cookie": f"session={self._session}", "User-Agent": USER_AGENT}

    def _request(self, path: str, data: dict[str, str] | None = None) -> bytes:
        return urllib.request.urlopen(
            urllib.request.Request(
                f"{BASE_URL}/{path}",
                headers=self._headers,
                data=None if data is None else urllib.parse.urlencode(data).encode(),
            )
        ).read()

    def fetch_input(self, year: int, day: int) -> typing.TextIO:
        year_path = os.path.join(self._cache, str(year))
        day_path = os.path.join(year_path, f"{day:02d}")

        if os.path.exists(day_path):
            return open(day_path, "r")

        os.makedirs(year_path, exist_ok=True)

        content = self._request(f"{year}/day/{day}/input")

        with open(day_path, "wb") as f:
            f.write(content)

        return io.StringIO(content.decode())

    def submit_answer(self, year: int, day: int, part: int, answer: str):
        parser = SubmitResultParser()
        parser.feed(
            self._request(
                f"{year}/day/{day}/answer", data={"level": str(part), "answer": answer}
            ).decode()
        )
        print("\n\n".join(parser.paragraphs))


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
