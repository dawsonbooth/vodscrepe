# `vodscrepe`

[![pypi version](http://img.shields.io/pypi/v/vodscrepe.svg?style=flat)](https://pypi.org/project/vodscrepe/ "View this project on PyPI")

# Description

This PyPI package is best described as a tool for scraping the <a href="vods.co">vods.co</a> website. Currently, the package only supports Super Smash Bros. Melee vods.

# Installation

With Python installed (https://www.python.org/downloads/), simply run the following command to add the package to your project.

```bash
pip install vodscrepe
```

# Usage

The following is an example usage of the package, which is also included in the repo as `example.py`:

```python
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

```

This example lists information about the vods from the most recent to page 300 in the following fashion:

```
"['2019-11-17'] DreamHack Atlanta 2019 - Mew2King (Sheik, Fox) vs Captain Faceroll (Sheik) - Grand Finals - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - n0ne (Captain Falcon) vs Captain Faceroll (Sheik) - Losers Finals - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Spark (CA) (Sheik) vs Captain Faceroll (Sheik) - Losers Semis - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - n0ne (Captain Falcon) vs Mew2King (Sheik) - Winners Finals - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Spark (CA) (Sheik) vs S2J (Captain Falcon) - Losers Quarters - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Captain Faceroll (Sheik) vs Kalvar (Marth) - Losers Quarters - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - n0ne (Captain Falcon) vs S2J (Captain Falcon) - Winners Semis - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Captain Faceroll (Sheik) vs Mew2King (Sheik) - Winners Semis - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Spark (CA) (Sheik) vs TheSWOOPER (Samus) - Losers Top 8 - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Voo (Falco) vs Kalvar (Marth) - Losers Top 8 - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - HiFi (Jigglypuff) vs TheSWOOPER (Samus) - Losers Round 3 - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Colbol (Fox) vs Kalvar (Marth) - Losers Round 3 - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Spark (CA) (Sheik) vs Captain Faceroll (Sheik) - Winners Quarters - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - S2J (Captain Falcon) vs Colbol (Fox) - Winners Quarters - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - n0ne (Captain Falcon) vs A Rookie (Mario) - Winners Quarters - Bo5"
"['2019-11-17'] DreamHack Atlanta 2019 - Mew2King (Fox) vs HiFi (Jigglypuff) - Winners Quarters - Bo5"
"['2019-11-09'] Genesis: BLACK - Lucky (Fox) vs S2J (Captain Falcon) - Grand Finals - Bo5"
"['2019-11-09'] Genesis: BLACK - Lucky (Fox) vs Captain Faceroll (Sheik) - Losers Finals - Bo5"
"['2019-11-09'] Genesis: BLACK - Lucky (Fox) vs KoDoRiN (Marth) - Losers Semis - Bo5"
"['2019-11-09'] Genesis: BLACK - S2J (Captain Falcon) vs Captain Faceroll (Sheik) - Winners Finals - Bo5"
"['2019-11-09'] Genesis: BLACK - Lucky (Fox) vs Panda (FL) (Fox) - Losers Quarters - Bo5"
"['2019-11-09'] Genesis: BLACK - Blassy (Fox) vs KoDoRiN (Marth) - Losers Quarters - Bo5"
"['2019-11-09'] Genesis: BLACK - Lucky (Fox) vs Captain Faceroll (Sheik) - Winners Semis - Bo5"
"['2019-11-09'] Genesis: BLACK - S2J (Captain Falcon) vs Blassy (Fox) - Winners Semis - Bo5"
Scraping terminated.
All vods:   0%|                                                             | 0/300 [00:14<?, ?pages/s]
Page 0:  40%|█████████████████████████████                                  | 24/60 [00:14<00:22,  1.62vods/s]
```
