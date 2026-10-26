# The Marathon Performance Continuum

Fits the full finish-time distribution of the 2014 Boston Marathon (31,842 runners) and places the 2:00:35 world record on it, with an Extreme Value Theory model of the fast tail.

[Live site](https://lyhjeremy.github.io/marathon-performance-continuum/) · [Write-up](https://lyhjeremy.github.io/marathon-performance-continuum/overview/)

Design and copy follow [these standards](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md).

## Results

| Measure | Value |
|---|---|
| Finishers faster than the 2:00:35 record | 0 of 31,842 (winner: 2:09) |
| Record's distance from the field mean | 2.4 standard deviations below (mean 4:03, SD 51 min) |
| Median finish, and its gap to the record | 3:52, 93% slower |
| Generalized Pareto shape on the fastest 5% | ξ = −0.147 (bounded tail) |

<p align="center">
  <img src="figures/continuum.png" alt="Histogram of 31,842 Boston 2014 finish times with a log-normal fit; the 2:00:35 world record line sits left of the whole field, including the winner's 2:09." width="820">
</p>

## Method

1. Body of the field: a shifted log-normal (floor 118 minutes) fitted with `scipy.stats.lognorm`. The field is right-skewed, peaking around 3:30 to 3:50.
2. The record against the field: counted empirically (how many finishers beat it) and as a z-score. The record's rarity as "1 in N" is not quoted, because that would rely on the fitted density far beyond the data.
3. Fast tail: Peaks-Over-Threshold Extreme Value Theory. The threshold is the fastest 5% of finishers (2:56, 1,593 runners), and a generalized Pareto distribution is fitted to how far each one beat it. A negative shape parameter means the tail has a finite end. No endpoint ("fastest possible time") is reported, since POT endpoint estimates are unstable.
4. Lookup: for reference times from 2:05 to 6:00, the share of the field finishing behind and the percent gap to the record (`tables/you_vs_goat.csv`). A 3:00 finishes ahead of 92.6% of this field; a 4:00 is ahead of 43.2%.

Stack: Python, pandas, NumPy, SciPy, matplotlib.

## How to run

```bash
pip install -r requirements.txt
python fetch_data.py      # Boston 2014 finishers -> data/raw/ (gitignored)
python analyze.py         # fits, lookup table and figures -> figures/ and tables/
```

## Repo layout

| Path | What it is |
|---|---|
| `fetch_data.py` | Downloads Boston 2014 results and keeps runners only (no wheelchair or handcycle), 2 to 7 hours |
| `analyze.py` | Log-normal fit, record placement, generalized Pareto tail fit, percentile lookup, figures |
| `figures/` | Field distribution with the record, tail fit, percentile curve |
| `tables/` | `summary.csv`, `you_vs_goat.csv` |
| `index.html`, `overview/` | The GitHub Pages site |

## Limitations

- Boston is a qualifying race, so this field is faster than a general-entry marathon. Every percentile describes this field only. A slower field would put the record further out.
- One race, one year (2014). The 2013 race was stopped partway and is left out.
- The record is set in `analyze.py` as Kelvin Kiptum's 2:00:35 (Chicago, 2023). A faster record changes that one mark and none of the field statistics.

## License

[MIT](LICENSE) © 2026 Jeremy Lee. Finisher data from [llimllib/bostonmarathon](https://github.com/llimllib/bostonmarathon).
