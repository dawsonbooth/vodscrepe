import re
import sys

import requests
from bs4 import BeautifulSoup, SoupStrainer
from tqdm import tqdm

from .aliases import guess_character
from .errors import InvalidVideoException
from .utils import build_url

stderr = lambda *args: print(file=sys.stderr, *args)

class Scraper:
    def __init__(self, video_game, event='', player1='', player2='', character1='', character2=''):
        self.video_game = video_game
        self.event = event
        self.player1 = player1
        self.player2 = player2
        self.character1 = character1
        self.character2 = character2
        self.base_url = build_url(video_game, event, player1,
                                  player2, character1, character2)

        self.session = requests.Session()

        page_content = self.urlopen(self.base_url)
        page_soup = BeautifulSoup(page_content, "lxml")
        sections = [h2.parent for h2 in page_soup.findChildren(
            "h2", class_="pane-title block-title")]

        self.characters = [o.getText()[1:]
                           for o in sections[0].findChildren("option")[1:]]
        self.players = [o.getText()[1:]
                        for o in sections[1].findChildren("option")[1:]]
        self.events = [o.getText()[1:]
                       for o in sections[2].findChildren("option")[1:]]
        self.players = [o.getText()[1:]
                        for o in sections[3].findChildren("option")[1:]]

        self.num_pages = 1
        last_page_tag = page_soup.findChild("a", title="Go to last page")
        if last_page_tag is not None:
            self.num_pages = int(
                re.search(r"=([\d]+)", last_page_tag["href"]).group(1))

    def urlopen(self, url):
        headers = {'Accept-Encoding': 'gzip'}

        response = self.session.get(url, headers=headers)
        return response.content

    def get_video_ids(self, vod_id: str, verbose: bool):
        vod_content = self.urlopen("https://vods.co/v/" + vod_id)
        vod_strainer = SoupStrainer('div', class_="region-inner clearfix")
        vod_soup = BeautifulSoup(
            vod_content, "lxml", parse_only=vod_strainer)
        content = vod_soup.findChild(recursive=False)

        try:
            video_ids = [v["data-vod"][:-1] for v in content.findChildren(
                "div", class_="js-video widescreen", recursive=False)]
            return video_ids
        except KeyError:
            raise InvalidVideoException(vod_id)

    def scrape_page(self, page_url, verbose: bool):
        page_content = self.urlopen(page_url)
        page_strainer = SoupStrainer("table")
        page_soup = BeautifulSoup(
            page_content, "lxml", parse_only=page_strainer)

        for table in page_soup.findChildren(recursive=False):
            date = table.caption.span.getText()
            for row in table.tbody.findChildren(recursive=False):
                cells = row.findChildren(recursive=False)

                try:
                    best_of = re.search(r"\d|$", cells[3].getText()).group()
                    if best_of is None:
                        continue

                    players = []
                    player = {"name": "Unknown", "characters": []}
                    for tag in cells[1].a.span.findChildren(recursive=False):
                        if tag.name == u'b':
                            if len(player["characters"]) != 0:
                                players.append(player)
                                player = {"name": "Unknown", "characters": []}
                            player["name"] = tag.getText()
                        elif tag.name == u'img':
                            player["characters"].append(
                                guess_character(tag["src"][24:-4]))
                    players.append(player)

                    vod_id = re.search(
                        r".*\/(.*)", cells[1].a["href"]).group(1)

                    yield {
                        "vod_id": vod_id,
                        "video_ids": self.get_video_ids(vod_id, verbose),
                        "date": date,
                        "tournament": re.search(r"[^\s].*[^\s]", cells[0].getText()).group(),
                        "players": players,
                        "round": re.search(r"[^\s].*[^\s]", cells[4].getText()).group(),
                        "best_of": best_of
                    }
                except InvalidVideoException as e:
                    if verbose:
                        stderr(e)
                    continue

    def scrape(self, pages=None, show_progress=False, verbose=False):
        if pages is None:
            pages = range(self.num_pages - 1)

        if show_progress:
            pages = tqdm(pages, position=1, unit='pages', desc="All vods")

        for page in pages:
            url = self.base_url + "?page=" + str(page)

            vods = self.scrape_page(url, verbose)
            if show_progress:
                vods = tqdm(vods, position=0, unit='vods',
                            desc="Page %d" % page, total=60)

            for vod in vods:
                yield vod
