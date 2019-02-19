from vodscrepe import Scraper

s = Scraper('melee')

pages = range(300)
for vod in s.scrape(pages):
    print(vod.video_id)
    if vod is not None:
        print(vod)
