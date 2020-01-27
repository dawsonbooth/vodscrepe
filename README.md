# `vodscrepe`

[![](https://img.shields.io/pypi/v/vodscrepe.svg?style=flat)](https://pypi.org/pypi/vodscrepe/)
[![](https://img.shields.io/pypi/dw/vodscrepe.svg?style=flat)](https://pypi.org/pypi/vodscrepe/)
[![](https://img.shields.io/pypi/pyversions/vodscrepe.svg?style=flat)](https://pypi.org/pypi/vodscrepe/)
[![](https://img.shields.io/pypi/format/vodscrepe.svg?style=flat)](https://pypi.org/pypi/vodscrepe/)
[![](https://img.shields.io/pypi/l/vodscrepe.svg?style=flat)](https://github.com/dawsonbooth/vodscrepe/blob/master/LICENSE)

# Description

This PyPI package is best described as a tool for scraping the [vods.co](https://vods.co/) website. Currently, the package only supports Super Smash Bros. Melee vods.

# Installation

With [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.

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

```bash
python example.py > sets.txt
```

Then, the `sets.txt` file becomes populated with vod information...

```txt
"['2020-01-26'] Genesis 7 - Zain (Marth) vs Hungrybox (Jigglypuff) - Grand Finals - Bo5"
"['2020-01-26'] Genesis 7 - Mango (Fox) vs Hungrybox (Jigglypuff) - Losers Finals - Bo5"
"['2020-01-26'] Genesis 7 - Hax (Fox) vs Hungrybox (Jigglypuff) - Losers Semis - Bo5"
"['2020-01-26'] Genesis 7 - Mango (Falco) vs Zain (Marth) - Winners Finals - Bo5"
"['2020-01-26'] Genesis 7 - Fiction (Fox) vs Hungrybox (Jigglypuff) - Losers Quarters - Bo5"
"['2020-01-26'] Genesis 7 - Hax (Fox) vs Leffen (Fox) - Losers Quarters - Bo5"
"['2020-01-26'] Genesis 7 - Hungrybox (Jigglypuff) vs Zain (Marth) - Winners Semis - Bo5"
"['2020-01-26'] Genesis 7 - Leffen (Fox) vs Mango (Falco) - Winners Semis - Bo5"
"['2020-01-26'] Genesis 7 - Fiction (Fox) vs n0ne (Captain Falcon) - Losers Top 8 - Bo5"
"['2020-01-26'] Genesis 7 - Hax (Fox) vs Shroomed (Sheik) - Losers Top 8 - Bo5"
"['2020-01-26'] Genesis 7 - n0ne (Captain Falcon) vs aMSa (Sheik) - Losers Round 6 - Bo5"
"['2020-01-26'] Genesis 7 - Fiction (Fox) vs Captain Faceroll (Sheik) - Losers Round 6 - Bo5"
"['2020-01-26'] Genesis 7 - Hax (Fox) vs PewPewU (Marth) - Losers Round 6 - Bo5"
"['2020-01-26'] Genesis 7 - Shroomed (Sheik) vs Swedish Delight (Sheik) - Losers Round 6 - Bo5"
"['2020-01-26'] Genesis 7 - iBDW (Fox) vs Captain Faceroll (Sheik) - Losers Round 5 - Bo5"
"['2020-01-26'] Genesis 7 - Ryobeat (Peach) vs S2J (Captain Falcon) - Losers Round 4 - Bo5"
"['2020-01-26'] Genesis 7 - Mew2King (Marth) vs ARMY (Ice Climbers) - Losers Round 4 - Bo5"
"['2020-01-26'] Genesis 7 - Trif (Peach) vs Swedish Delight (Sheik) - Losers Round 4 - Bo5"
"['2020-01-26'] Genesis 7 - SFAT (Fox) vs Panda (FL) (Fox) - Losers Round 3 - Bo5"
"['2020-01-26'] Genesis 7 - Shroomed (Sheik) vs Zain (Marth) - Winners Quarters - Bo5"
"['2020-01-26'] Genesis 7 - Mango (Falco) vs aMSa (Sheik) - Winners Quarters - Bo5"
"['2020-01-26'] Genesis 7 - Fiction (Fox) vs Leffen (Fox) - Winners Quarters - Bo3"
Scraping terminated.
```

...while the terminal details the progress:

```bash
All vods:   0%|                                              | 0/300 [00:07<?, ?pages/s]
Page 0:  37%|████████████████████                            | 22/60 [00:07<00:12,  3.07vods/s]
```

# License

This software is released under the terms of [MIT license](LICENSE).
