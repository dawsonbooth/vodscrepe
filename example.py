from vodscrepe import Scraper
from tqdm import tqdm

s = Scraper('melee')

pages = range(300)
for vod in s.scrape(pages, show_progress=True):
    if vod is not None:
        pass
        # tqdm.write(str(vod))
