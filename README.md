# lottoguesser

**The pattern is that there is no pattern.**

A deliberately honest lottery number lab. A fair draw carries no signal to
learn, so this tool does not predict winning numbers — it can't, and neither
can anything else. Instead it gives you the only real edge that exists: it
helps you **stop picking like a human**. It spreads picks across the number
space, cuts birthday/popular-sequence clustering, and turns real draw history
into transparent weighting — so on the vanishingly rare chance you win, you
split the jackpot with fewer people.

**Live:** <https://grassclaw.github.io/lottoguesser/> — [the reasoning probe](https://grassclaw.github.io/lottoguesser/study/) · [the lab](https://grassclaw.github.io/lottoguesser/app/)

## The point: a reasoning probe

The lottery is the **instrument**, not the subject. It is the rare task where
impossibility is *provable* (independent draws carry zero signal), so it cleanly
grades what a reasoning engine does when it can't bluff: **deflect** into life
advice, **capitulate** into fake confidence, or **reframe** — recognize there is
no signal and pivot to the part that is actually solvable (human picking
behavior). Number-matches are kept as a deliberate **control** — luck, not
reasoning — to prove that a model which "wins" didn't think better.

[![The reasoning-probe study dashboard](media/study.png)](https://grassclaw.github.io/lottoguesser/study/)

Each engine is run through a two-phase protocol (bare task → theory handed over)
and classified. Details: [`study/PROTOCOL.md`](study/PROTOCOL.md) · dashboard:
[`study/`](study/) · runner: [`study/runner/`](study/runner/). The seed run is
Claude Opus 4.8 probing itself (a flagged confound).

## The lab

The same thesis, made usable: it can't predict a draw, so it helps you pick
*unlike a human* — spread across the board, dodge birthday and popular-sequence
clustering, grade saved picks against real draws.

[![The Lottery Guesser lab generating Powerball tickets](media/app.png)](https://grassclaw.github.io/lottoguesser/app/)

## The two eras of this project

This repo is the merge of two attempts, kept on purpose as a record of the idea:

- **v1 — `lotto_v1.py` (2024).** Trained a `RandomForestClassifier` to forecast
  Powerball. It couldn't. There is no function from past draws to future draws
  in a fair lottery, so the model was learning noise. That failure *is* the
  thesis: the honest move is to flip the target.
- **v2 — `app/` (2026).** A single-file, dependency-free browser app that
  optimizes for the **antipattern of human randomness** rather than pretending
  to predict. This is the centerpiece now.

The predict → record → compare → learn loop from v1 (`compare_learn.py`,
`tools/db/`) survives in v2 as **Save + Previous Guess Tuner**: save a generated
set, and after the next real draw the app scores how your picks actually did and
nudges the filters.

## Run it

Open `app/index.html` in a browser. No build, no server, no dependencies.

```
open app/index.html
```

- **Controls** — game, ticket count, candidate pool, optimization target
  (Balanced / Low overlap / History-weighted), and filters for spread, parity,
  birthday avoidance, consecutive runs, and ticket diversity.
- **Guesses** — scored tickets, plus the Previous Guess Tuner that grades saved
  picks against the latest real draw. `Tuner` and `ROI` open companion tools.
- **Data Lab** — paste/load draw history, see the number-pressure heatmap and a
  cluster-switching read (carry-over repeats, lag-two echoes, rolling cores).

## Games & data

Bundled history (in `app/history.js`):

- **Powerball** (5 of 69 + 1 of 26) and **Mega Millions** (5 of 70 + 1 of 24) —
  180-day windows from the original 2024 CSVs in `historical_data/`.
- **Arizona** The Pick / Fantasy 5 / Triple Twist — scraped via
  `app/refresh-history.sh` (Arizona Lottery past-180-days PDFs → `history.js`).
- **Classic 6/49** and a **custom** main-only game.

Paste your own draws (one per line) into the Data Lab to weight any game.

## Repo layout

```
app/                     v2 web app (the project today)
  index.html             the lab
  history.js             bundled draw history (PB, Mega, AZ)
  comparison-tuner.html  position-aware comparison tool
  roi-analyzer.html      expected-value-by-game comparison
  refresh-history.sh     re-pull Arizona PDFs into history.js
historical_data/         original 2024 CSV/PDF draw data
lotto_v1.py              v1 ML predictor (kept as a record of the thesis)
compare_learn.py         v1 predict/compare loop
tools/                   v1 PDF→CSV + SQLite store helpers
```

## The honest disclaimer

Every valid combination is exactly as likely as every other. This app changes
**which humans you share a prize with**, never your odds of winning one. It is a
toy and a thesis, not a strategy for making money.
</content>
