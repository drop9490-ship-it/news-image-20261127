# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/drop9490-ship-it/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/drop9490-ship-it/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

Friday 27 November 2026: 35 stories, 7 regions, 15 fields — one day of world news in one image. A diesel tanker capsizes off Ibiza, Gukesh and Sindarov draw a marathon Game 3 in Geneva, and Amazon workers strike in 20+ countries on Black Friday. Every story was first reported on 27 November 2026 in some time zone; six older stories were deliberately left out — see DATE CHECK on the poster.

## Run it

```sh
python3 render.py            # rebuilds entry.png from illu/ (needs Pillow)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

`main.py` is standard library only: the grading server just copies the
pre-rendered `entry.png`. `NEWS.md` documents all 35 stories, the region
bar, the by-the-numbers checks and the DATE CHECK exclusions.

---

<sub>Entered on [make.fun](https://make.fun/?ref=9ncycshz&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
