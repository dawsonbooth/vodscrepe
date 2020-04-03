from tqdm import tqdm

from vodscrepe import Scraper, formatted_title

s = Scraper('melee')

try:
    for vod in s.scrape(show_progress=True):
        if vod is not None:
            tqdm.write(formatted_title(vod))
except KeyboardInterrupt:
    tqdm.write("Scraping terminated.")
