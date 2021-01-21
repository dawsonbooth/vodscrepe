import argparse
import dataclasses as dc
import json

from tqdm import tqdm

from . import Scraper


def main():
    parser = argparse.ArgumentParser(description="Scrape the vods from http://vods.co/")
    parser.add_argument("game", type=str, default="melee", help="The game whose vods will be scraped")
    parser.add_argument("-f", "--first", type=int, default=0, help="First page of scraping")
    parser.add_argument("-l", "--last", type=int, default=1000, help="Last page of scraping")
    parser.add_argument("-p1", "--player1", type=str, default="", help="Player 1")
    parser.add_argument("-p2", "--player2", type=str, default="", help="Player 2")
    parser.add_argument("-c1", "--character1", type=str, default="", help="Character 1")
    parser.add_argument("-c2", "--character2", type=str, default="", help="Character 2")
    parser.add_argument("-e", "--event", type=str, default="", help="Event")
    parser.add_argument("-ca1", "--caster1", type=str, default="", help="Caster 1")
    parser.add_argument("-ca2", "--caster2", type=str, default="", help="Caster 2")
    parser.add_argument("-p", "--progress", action="store_true", help="Display scraping progress")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display error statements")
    parser.add_argument("-j", "--json", action="store_true", help="Output vod with JSON format")
    parser.add_argument("-w", "--workers", type=int, default=10, help="Number of workers")
    parser.add_argument("-pw", "--page-workers", type=int, default=2, help="Number of page workers")

    args = parser.parse_args()

    s = Scraper(
        args.game,
        event=args.event,
        player1=args.player1,
        player2=args.player2,
        character1=args.character1,
        character2=args.character2,
        caster1=args.caster1,
        caster2=args.caster2,
        num_workers=args.workers,
        num_page_workers=args.page_workers,
        verbose=args.verbose,
    )

    pages = range(args.first, min(s.num_pages - 1, args.last))
    try:
        if args.json:
            tqdm.write("[")
        for vod in s.scrape(pages, show_progress=args.progress):
            if vod is not None:
                if args.json:
                    tqdm.write(f"{json.dumps(dc.asdict(vod), indent=None)},")
                else:
                    tqdm.write(str(vod))
    except KeyboardInterrupt:
        if args.json:
            tqdm.write("]")


if __name__ == "__main__":
    main()
