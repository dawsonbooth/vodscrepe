from __future__ import annotations

import re
import sys
from concurrent.futures import Future
from dataclasses import dataclass
from queue import Queue
from typing import Generator, List, Sequence, Tuple

from bs4 import BeautifulSoup, SoupStrainer
from requests_futures.sessions import FuturesSession
from tqdm import tqdm

from vodscrepe.vod import Vod

from .aliases import guess_character
from .errors import InvalidVideoError


class Scraper:
    __slots__ = "base_url", "num_workers", "num_page_workers", "session", "num_pages", "verbose"

    base_url: URL
    num_workers: int
    num_page_workers: int
    session: FuturesSession
    num_pages: int
    verbose: bool

    def __init__(
        self,
        video_game: str,
        event: str = "",
        player1: str = "",
        player2: str = "",
        character1: str = "",
        character2: str = "",
        caster1: str = "",
        caster2: str = "",
        num_workers: int = 10,
        num_page_workers: int = 2,
        verbose: bool = False,
    ):
        self.base_url = self.URL(video_game, event, player1, player2, character1, character2, caster1, caster2)

        self.num_workers = num_workers
        self.num_page_workers = min(num_page_workers, self.num_workers)
        self.session = FuturesSession(max_workers=self.num_workers)

        page_content = self.request(str(self.base_url)).result().content
        page_soup = BeautifulSoup(page_content, "lxml")

        self.num_pages = 1
        last_page_tag = page_soup.findChild("a", title="Go to last page")
        if last_page_tag:
            self.num_pages = int(re.search(r"page=([\d]+)", last_page_tag["href"]).group(1))

        self.verbose = verbose

    def request(self, url: str) -> Future:
        return self.session.get(url, headers={"Accept-Encoding": "gzip"})

    def scrape_vod_page(self, vod_id: str, vod_request: Future) -> Tuple[List[str], List[Vod.Caster]]:
        vod_content = vod_request.result().content
        vod_strainer = SoupStrainer("div", class_="region-inner clearfix")
        vod_soup = BeautifulSoup(vod_content, "lxml", parse_only=vod_strainer)
        content = vod_soup.findChild(recursive=False)

        try:
            video_ids = [
                re.search(r"^([^?]*)", v["data-vod"]).group(1)
                for v in content.findChildren("div", class_="js-video widescreen", recursive=False)
            ]
            if len(video_ids) == 0:
                raise InvalidVideoError(vod_id)

            casters = []
            casters_tag = content.findChild("div", class_="field-items")
            if casters_tag:
                casters = [Vod.Caster(c.getText()) for c in casters_tag.findChildren(recursive=False)]
            return (video_ids, casters)
        except KeyError:
            raise InvalidVideoError(vod_id)

    def scrape_page(self, page_request: Future) -> Generator[Vod, None, None]:
        page_content = page_request.result().content
        page_strainer = SoupStrainer("table")
        page_soup = BeautifulSoup(page_content, "lxml", parse_only=page_strainer)

        vod_requests = [self.request(tr.findChild("a")["href"]) for tr in page_soup.findChildren("tr")]

        for table in page_soup.findChildren(recursive=False):
            date = table.caption.span.getText()
            for i, row in enumerate(table.tbody.findChildren(recursive=False)):
                cells = row.findChildren(recursive=False)

                try:
                    vod_id = re.search(r".*\/(.*)", cells[1].a["href"]).group(1)

                    try:
                        best_of = int(re.search(r"Bo([\d]*)", cells[3].getText()).group(1))
                    except AttributeError:
                        continue

                    players = []
                    player = Vod.Player("Unknown", [])
                    for tag in cells[1].a.span.findChildren(recursive=False):
                        if tag.name == "b":
                            if len(player.characters) != 0:
                                players.append(player)
                                player = Vod.Player("Unknown", [])
                            player.alias = tag.getText()
                        elif tag.name == "img":
                            player.characters.append(guess_character(tag["src"][24:-4]))
                    players.append(player)

                    video_ids, casters = self.scrape_vod_page(vod_id, vod_requests[i])

                    tournament = re.search(r"[^\s].*[^\s]", cells[0].getText()).group()
                    _round = re.search(r"[^\s].*[^\s]", cells[4].getText()).group()

                    yield Vod(vod_id, video_ids, date, tournament, players, casters, _round, best_of)
                except InvalidVideoError as e:
                    if self.verbose:
                        print(e, file=sys.stderr)

    def scrape(self, pages: Sequence[int] = [], show_progress: bool = False) -> Generator[Vod, None, None]:
        if not pages:
            pages = range(self.num_pages - 1)

        self.num_page_workers = min(self.num_page_workers, len(pages))

        request_queue: Queue[Future] = Queue(self.num_page_workers)
        for i in range(self.num_page_workers):
            request_queue.put(self.request(f"{self.base_url}?page={pages[i]}"))

        if show_progress:
            pages = tqdm(pages, position=1, unit="pages", desc="All vods")

        for page in pages:
            vods = self.scrape_page(request_queue.get())
            if show_progress:
                vods = tqdm(vods, position=0, unit="vods", desc=f"Page {page}", total=60)

            for vod in vods:
                yield vod

            request_queue.put(self.request(f"{self.base_url}?page={page + self.num_page_workers}"))

    @dataclass
    class URL:
        video_game: str
        event: str = ""
        player1: str = ""
        player2: str = ""
        character1: str = ""
        character2: str = ""
        caster1: str = ""
        caster2: str = ""

        def __str__(self) -> str:
            url = "https://vods.co/" + self.video_game
            if self.player1:
                url += "/player/" + self.player1
            if self.player2:
                url += "/player2/" + self.player2
            if self.event:
                url += "/event/" + self.event
            if self.character1:
                url += "/character/" + self.character1
            if self.character2:
                url += "/character2/" + self.character2
            if self.caster1:
                url += "/caster/" + self.character1
            if self.caster2:
                url += "/caster2/" + self.character2
            return url
