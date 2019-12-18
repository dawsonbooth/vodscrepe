import gzip
import re
import urllib.request
from urllib.error import HTTPError, URLError

import lxml
from bs4 import BeautifulSoup, SoupStrainer
from tqdm import tqdm

from .aliases import *
from .errors import *
from .vod import Vod


def urlopen(url, debug=False):
    headers = {'Accept': 'application/xhtml+xml',
               'Accept-Encoding': 'gzip'}
    req = urllib.request.Request(url, headers=headers)

    response = None
    while response is None:
        try:
            response = urllib.request.urlopen(req)
        except (URLError, HTTPError):
            if debug:
                tqdm.write("Connection Error: Reconnecting to '%s'" % url)
            continue
    return gzip.decompress(response.read())


# TODO: Scrape vods.co for list of chars, player names, tournaments, etc.

class Scraper():
    def __init__(self, game, debug=False):
        self.home_url = "https://vods.co"
        self.game = game
        self.page = 0
        self.debug = debug

    def scrape_vod(self, vod_url: str, platform='youtube'):
        vod_content = urlopen(vod_url, self.debug)
        vod_strainer = SoupStrainer('div')
        vod_soup = BeautifulSoup(vod_content, "lxml", parse_only=vod_strainer)
        video_tag = vod_soup.find("div", class_="js-video widescreen", id="g1")
        if video_tag is None:
            return None
        title_tag = vod_soup.find("div", class_="block-title")
        vod_title = title_tag.get_text().replace('  ', ' ')

        # Create vod object
        vod = Vod()

        # VOD properties
        vod.vod_id = vod_url[18:]
        vod.video_id = video_tag["data-vod"].split("?")[0]
        vod.platform = 'youtube'
        # TODO: Support Twitch vods

        # Parse title for svp Vod info
        vod.parse_title(vod_title)

        return vod

    def _scrape_page(self, page_url, platform='youtube'):
        # Page soup
        page_content = urlopen(page_url, self.debug)
        page_strainer = SoupStrainer("tr", class_=re.compile("recency"))
        page_soup = BeautifulSoup(
            page_content, "lxml", parse_only=page_strainer)

        if page_soup.findChild('tr') is None:
            yield None

        for row in page_soup.findChildren("tr"):
            cells = [cell for cell in row.findChildren("td")]

            # Check Match Format
            match_format = cells[3].get_text().strip()
            if re.match("Bo\d", match_format) is None:
                continue

            # Create VOD
            try:
                vod = self.scrape_vod(
                    cells[1].a["href"], platform=platform)
            except InvalidVideoError as e:
                if self.debug:
                    tqdm.write(e)
                continue

            if vod is None:
                continue

            # Characters
            title_tag = cells[1].a.span
            num_chars_p1 = str(title_tag).split("vs")[0].count("img")
            characters = [char_img["src"][24:-4]
                          for char_img in title_tag.find_all(
                "img", recursive=False)]
            vod.player1.characters = [character(
                c) for c in characters[:num_chars_p1]]
            if None in vod.player1.characters:
                vod.player1.characters = []
            vod.player2.characters = [character(
                c) for c in characters[num_chars_p1:]]
            if None in vod.player2.characters:
                vod.player2.characters = []

            yield vod

    def scrape(self, pages=range(300), platform='youtube', event='',
               player1='', player2='', character1='', character2='',
               show_progress=True):

        page_url = self.home_url + "/" + self.game
        if player1:
            page_url += "/player/" + player1
        if player2:
            page_url += "/player2/" + player2
        if event:
            page_url += "/event/" + event
        if character1:
            page_url += "/character/" + character1
        if character2:
            page_url += "/character2/" + character2

        page_url = page_url.replace(' ', '%20')

        if show_progress:
            pages = tqdm(pages, position=1, unit='pages', desc="All vods")

        for page in pages:
            self.page = page
            url = page_url if page == 0 else page_url + "?page=" + str(page)

            vods = self._scrape_page(url, platform=platform)
            if show_progress:
                vods = tqdm(vods, position=0, unit='vods',
                            desc="Page %d" % page, total=60)

            for vod in vods:
                if vod is None:
                    return None
                yield vod
