from tqdm import tqdm

from vodscrepe import Scraper

s = Scraper("melee")

try:
    for vod in s.scrape(show_progress=True):
        if vod is not None:
            tqdm.write(str(vod))
except KeyboardInterrupt:
    tqdm.write("Scraping terminated.")
