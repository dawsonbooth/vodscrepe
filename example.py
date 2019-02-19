from vodscrepe import Scraper, Database

db = Database('vods.db', 'vods')

s = Scraper('melee')

pages = range(300)
for vod in s.scrape(pages):
    print(vod.video_id)
    if vod is None:
        break
    if not db.contains(vod):
        db.save(vod)
