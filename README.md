# The World Today — Sunday 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/ELGANTENG/news-image-22-november/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/ELGANTENG/news-image-22-november/reward.svg)](https://make.fun/bounty/news-image-20261122)

A newspaper-style front page summing up Sunday 22 November 2026 in one
image: one hero story and six more panels, drawn programmatically with
Python and PIL — no photos, no external images, fully deterministic.

## The seven stories

1. **COP31 close to a deal at last (hero)** — After two days of overtime,
   a new climate package goes to nearly 200 nations for approval on Sunday
   morning in Antalya. *Source: Reuters, 22 Nov 2026.*
2. **Nepal's PM lands in Delhi** — Balendra Shah begins his first foreign
   trip since taking office in March; talks with Narendra Modi on Monday.
   *Source: Reuters.*
3. **Pant's 128 puts India past 600** — Rishabh Pant's century powers India
   to 629 for 6 at lunch on day four in Wellington, a lead of 261.
   *Source: ESPNcricinfo live blog, 22 Nov 2026.*
4. **Baltic ship fire burns on** — The sanctioned Russian cargo ship
   Sparta II is still ablaze after a suspected Ukrainian drone strike.
   *Source: CNN / Reuters.*
5. **Big-city deals still unsigned** — Two weeks after South Africa's local
   elections, Johannesburg, Tshwane and Durban still have no governing deal.
   *Source: African Bulletin / BBC.*
6. **Blair: rejoin EU only on tech terms** — Tony Blair says Britain should
   rejoin the EU only if the bloc moves the right way on technology.
   *Source: BBC, 21–22 Nov 2026.*
7. **AI "solves" maths' hardest problem** — Mathematicians verify an
   AI-assisted proof of the Riemann Hypothesis, unsolved since 1859.
   *Source: The Wall Street Journal / AP.*

## How it works

`generate_image.py` draws the whole front page with PIL (DejaVu fonts,
fixed coordinates, no randomness, no network), writing `entry.png`
(1024×1024, under 1 MiB). Running it twice produces byte-identical output.

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `out`).
