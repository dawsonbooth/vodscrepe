import argparse

from tqdm import tqdm

from vodscrepe import Scraper, formatted_title


def main():

    parser = argparse.ArgumentParser(
        description='Scrape the vods from http://vods.co/')
    parser.add_argument('game', type=str,
                        help='The game whose vods will be scraped')
    parser.add_argument('-f', '--first', type=int, default=0,
                        help='First page of scraping')
    parser.add_argument('-l', '--last', type=int, default=1000,
                        help='Last page of scraping')
    parser.add_argument('-p1', '--player1', type=str, default="",
                        help='Player 1')
    parser.add_argument('-p2', '--player2', type=str, default="",
                        help='Player 2')
    parser.add_argument('-c1', '--char1', type=str, default="",
                        help='Character 1')
    parser.add_argument('-c2', '--char2', type=str, default="",
                        help='Character 2')
    parser.add_argument('-e', '--event', type=str, default="",
                        help='Event')
    parser.add_argument('-ca1', '--caster1', type=str, default="",
                        help='Caster 1')
    parser.add_argument('-ca2', '--caster2', type=str, default="",
                        help='Caster 2')
    parser.add_argument('-p', '--progress', type=bool, default=True,
                        help='Display scraping progress')
    parser.add_argument('-v', '--verbose', type=bool, default=False,
                        help='Display error statements')

    args = parser.parse_args()

    s = Scraper(args.game)

    pages = range(args.first, min(s.num_pages - 1, args.last))
    try:
        for vod in s.scrape(pages, show_progress=args.progress, verbose=args.verbose):
            if vod is not None:
                tqdm.write(formatted_title(vod))
    except KeyboardInterrupt:
        tqdm.write("Scraping terminated.")
