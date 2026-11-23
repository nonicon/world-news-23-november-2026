# World News in One Image — 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/nonicon/world-news-23-november-2026/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/nonicon/world-news-23-november-2026/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Entry for the make.fun competition
[`news-image-20261123`](https://make.fun/c/news-image-20261123)
("Sum up 23 November's world news in one image").

## What it is

`main.py` is a standard-library-only Python program. It paints a
one-page newspaper front page — masthead, lead story with a drawn map
of the Gulf, the collapsed climate talks, three more stories and a
round-up of briefs — and writes it as `entry.png` (1024x1024, about
22 KB). No image files, no fonts on disk, no network: every pixel is
drawn by the program itself with a hand-built 5x7 dot-matrix font,
so two runs produce byte-identical output.

## The day's news

Monday 23 November 2026, as reported overnight and in the morning
editions (CNN, Le Monde, The Times, WSJ, Euronews and wire reports):

- **Lead — the Gulf:** Iran fired drones and missiles at US military
  sites in Bahrain again; Bahrain said its defences stopped the
  attack, a civilian site caught fire, and tankers wait to test the
  US blockade of the Strait of Hormuz.
- **Climate:** COP31 in Antalya ended on Sunday with no deal — the EU
  rejected a pact that never mentioned fossil fuels, the first such
  collapse since Copenhagen in 2009.
- **Mexico:** forces captured FBI most-wanted cartel boss
  "El Chapo Isidro" after firefights in Sinaloa left 11 dead.
- **Seoul:** South Korea's education minister resigned amid an
  AI-driven exam cheating scandal.
- **United Nations:** countries agreed to keep negotiating rules for
  lethal autonomous weapons.
- **Also today:** a Russian cargo ship ablaze off Finland and 14
  missing near Kyiv; dozens missing after an Indonesian factory fire;
  thousands marching in Lisbon over living costs; Nepal's PM in talks
  with PM Modi and India's record 720 for 9 in Wellington; the FBI's
  crime database hacked; an Israeli minister calling settler violence
  "Jewish terrorism".

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

## License

MIT — see `LICENSE`.
