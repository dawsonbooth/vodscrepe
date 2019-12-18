from vodscrepe import Scraper
from tqdm import tqdm

s = Scraper('melee', debug=True)

pages = range(300)
try:
    for vod in s.scrape(pages, show_progress=True):
        if vod is not None:
            tqdm.write(str(vod))
except KeyboardInterrupt:
    tqdm.write("Scraping terminated.")
