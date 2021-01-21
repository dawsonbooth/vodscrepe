from __future__ import annotations

import re
import sys
from queue import Queue

from bs4 import BeautifulSoup, SoupStrainer
from requests.adapters import Response
from requests_futures.sessions import FuturesSession
from tqdm import tqdm

from vodscrepe.vod import Vod

from .aliases import guess_character
from .errors import InvalidVideoError


def build_url(
    video_game,
    event: str = "",
    player1: str = "",
    player2: str = "",
    character1: str = "",
    character2: str = "",
    caster1: str = "",
    caster2: str = "",
) -> str:
    url = "https://vods.co/" + video_game
    if player1:
        url += "/player/" + player1
    if player2:
        url += "/player2/" + player2
    if event:
        url += "/event/" + event
    if character1:
        url += "/character/" + character1
    if character2:
        url += "/character2/" + character2
    if caster1:
        url += "/caster/" + character1
    if caster2:
        url += "/caster2/" + character2
    return url


class Scraper:
    def __init__(
        self,
        video_game,
        event="",
        player1="",
        player2="",
        character1="",
        character2="",
        caster1="",
        caster2="",
        num_workers=10,
        num_page_workers=2,
    ):
        self.video_game = video_game
        self.event = event
        self.player1 = player1
        self.player2 = player2
        self.character1 = character1
        self.character2 = character2
        self.caster1 = caster1
        self.caster2 = caster2

        self.base_url = build_url(video_game, event, player1, player2, character1, character2, caster1, caster2)

        self.num_workers = num_workers
        self.num_page_workers = min(num_page_workers, self.num_workers)
        self.session = FuturesSession(max_workers=self.num_workers)

        page_content = self.request(self.base_url).result().content
        page_soup = BeautifulSoup(page_content, "lxml")
        sections = [h2.parent for h2 in page_soup.findChildren("h2", class_="pane-title block-title")]

        self.characters = [o.getText()[1:] for o in sections[0].findChildren("option")[1:]]
        self.players = [o.getText()[1:] for o in sections[1].findChildren("option")[1:]]
        self.events = [o.getText()[1:] for o in sections[2].findChildren("option")[1:]]
        self.casters = [o.getText()[1:] for o in sections[3].findChildren("option")[1:]]

        self.num_pages = 1
        last_page_tag = page_soup.findChild("a", title="Go to last page")
        if last_page_tag is not None:
            self.num_pages = int(re.search(r"page=([\d]+)", last_page_tag["href"]).group(1))

    def request(self, url: str) -> Response:
        return self.session.get(url, headers={"Accept-Encoding": "gzip"})

    def scrape_vod_page(self, vod_id: str, vod_request: Response, verbose: bool):
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

            casters_tag = content.findChild("div", class_="field-items")
            casters = []
            if casters_tag:
                casters = [{"alias": c.getText()} for c in casters_tag.findChildren(recursive=False)]
            return (video_ids, casters)
        except KeyError:
            raise InvalidVideoError(vod_id)

    def scrape_page(self, page_request, verbose: bool):
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
                    player = Vod.Player(**{"alias": "Unknown", "characters": []})
                    for tag in cells[1].a.span.findChildren(recursive=False):
                        if tag.name == "b":
                            if len(player.characters) != 0:
                                players.append(player)
                                player = Vod.Player(**{"alias": "Unknown", "characters": []})
                            player.alias = tag.getText()
                        elif tag.name == "img":
                            player.characters.append(guess_character(tag["src"][24:-4]))
                    players.append(player)

                    video_ids, casters = self.scrape_vod_page(vod_id, vod_requests[i], verbose)

                    yield Vod(
                        **{
                            "vod_id": vod_id,
                            "video_ids": video_ids,
                            "date": date,
                            "tournament": re.search(r"[^\s].*[^\s]", cells[0].getText()).group(),
                            "players": players,
                            "casters": casters,
                            "round": re.search(r"[^\s].*[^\s]", cells[4].getText()).group(),
                            "best_of": best_of,
                        }
                    )
                except InvalidVideoError as e:
                    if verbose:
                        print(e, file=sys.stderr)

    def scrape(self, pages=None, show_progress=False, verbose=False):
        if pages is None:
            pages = range(self.num_pages - 1)

        self.num_page_workers = min(self.num_page_workers, len(pages))

        request_queue = Queue(self.num_page_workers)
        for i in range(self.num_page_workers):
            request_queue.put(self.request(self.base_url + "?page=" + str(pages[i])))

        iter_pages = pages
        if show_progress:
            iter_pages = tqdm(iter_pages, position=1, unit="pages", desc="All vods")

        for page in iter_pages:

            vods = self.scrape_page(request_queue.get(), verbose)
            if show_progress:
                vods = tqdm(vods, position=0, unit="vods", desc=f"Page {page}", total=60)

            for vod in vods:
                yield vod

            request_queue.put(self.request(f"{self.base_url}?page={page + self.num_page_workers}"))
