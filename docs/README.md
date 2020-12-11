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
from tqdm import tqdm

from vodscrepe import Scraper, formatted_title

s = Scraper('melee')

try:
    for vod in s.scrape(show_progress=True):
        tqdm.write(formatted_title(vod))
except KeyboardInterrupt:
    tqdm.write("Scraping terminated.")
```

This example lists information about the vods from the most recent to the last page in the following fashion:

```bash
python example.py > sets.txt
```

Then, the `sets.txt` file becomes populated with vod information...

```txt
['2020-03-15'] CEO Dreamland 2020 - Colbol (Fox) vs Hungrybox (Jigglypuff) - Grand Finals - Bo5
['2020-03-15'] CEO Dreamland 2020 - Colbol (Fox) vs n0ne (Captain Falcon) - Losers Finals - Bo5
['2020-03-15'] CEO Dreamland 2020 - Colbol (Fox) vs Gahtzu (Captain Falcon) - Losers Semis - Bo5
['2020-03-15'] CEO Dreamland 2020 - Hungrybox (Jigglypuff) vs n0ne (Captain Falcon) - Winners Finals - Bo5
['2020-03-15'] CEO Dreamland 2020 - Panda (FL) (Fox) vs Gahtzu (Captain Falcon) - Losers Quarters - Bo5
['2020-03-15'] CEO Dreamland 2020 - Colbol (Fox) vs Chef Rach (Captain Falcon) - Losers Quarters - Bo5
['2020-03-15'] CEO Dreamland 2020 - n0ne (Captain Falcon) vs Panda (FL) (Fox) - Winners Semis - Bo5
['2020-03-15'] CEO Dreamland 2020 - Colbol (Fox) vs Hungrybox (Jigglypuff) - Winners Semis - Bo5
['2020-03-15'] CEO Dreamland 2020 - Krudo (Sheik) vs Gahtzu (Captain Falcon) - Losers Top 8 - Bo5
['2020-03-15'] CEO Dreamland 2020 - blankshooter744 (Fox) vs Chef Rach (Captain Falcon) - Losers Round 5 - Bo5
['2020-03-15'] CEO Dreamland 2020 - Leighton (Jigglypuff) vs Prof (Marth) - Losers Round 5 - Bo5
['2020-03-15'] CEO Dreamland 2020 - Sinbad (Sheik) vs Krudo (Sheik) - Losers Round 5 - Bo5
['2020-03-15'] CEO Dreamland 2020 - Wevans (Samus) vs Gahtzu (Captain Falcon) - Losers Round 5 - Bo5
['2020-03-15'] CEO Dreamland 2020 - Sinbad (Sheik) vs Dom (FL) (Marth) - Losers Round 4 - Bo5
['2020-03-15'] CEO Dreamland 2020 - Colbol (Fox) vs Gahtzu (Captain Falcon) - Winners Quarters - Bo5
Scraping terminated.
```

...while the terminal details the progress:

```bash
All vods:   0%|                                              | 0/331 [00:07<?, ?pages/s]
Page 0:  25%|██████████████                                  | 15/60 [00:07<00:12,  3.07vods/s]
```

# License

This software is released under the terms of [MIT license](LICENSE).
