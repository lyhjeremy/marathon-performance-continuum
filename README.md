# The Marathon Performance Continuum

Where does a 3:00 or a 4:00 marathon sit relative to the world record? This repo fits the finish-time distribution of all 31,842 runners in the 2014 Boston Marathon, marks Sabastian Sawe's 1:59:30 world record on the same axis, and models the fast tail with Extreme Value Theory.

[Live site](https://lyhjeremy.github.io/marathon-performance-continuum/) · [Write-up](https://lyhjeremy.github.io/marathon-performance-continuum/overview/)

Design and copy follow [these standards](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md).

## Results

| Measure | Value |
|---|---|
| Finishers faster than the 1:59:30 record | 0 of 31,842 (winner: 2:09) |
| Record's distance from the field mean | 2.4 standard deviations below (mean 4:03, SD 51 min) |
| Median finish, and its gap to the record | 3:52, 94% slower |
| Generalized Pareto shape on the fastest 5% | ξ = −0.147 (bounded tail) |

<p align="center">
  <img src="figures/continuum.png" alt="Histogram of 31,842 Boston 2014 finish times with a log-normal fit; the 1:59:30 world record line sits left of the whole field, including the winner's 2:09." width="820">
</p>

## Method

The body of the field is a shifted log-normal (floor 118 minutes) fitted with `scipy.stats.lognorm`; the field is right-skewed and peaks around 3:30 to 3:50. The record is placed against it two ways, by counting how many finishers beat it and as a z-score. Its rarity as "1 in N" is not quoted, because that would rely on the fitted density far beyond the data.

The fast tail uses Peaks-Over-Threshold Extreme Value Theory. The threshold is the fastest 5% of finishers (2:56, 1,593 runners), and a generalized Pareto distribution is fitted to how far each one beat it. A negative shape parameter means the tail has a finite end, but no endpoint ("fastest possible time") is reported, since POT endpoint estimates are unstable.

Last, a lookup table (`tables/you_vs_goat.csv`) gives, for reference times from 2:05 to 6:00, the share of the field finishing behind and the percent gap to the record. A 3:00 finishes ahead of 92.6% of this field and a 4:00 ahead of 43.2%. The [write-up](https://lyhjeremy.github.io/marathon-performance-continuum/overview/#you) does the same lookup for any time, optionally within one gender and Boston age group.

Stack: Python, pandas, NumPy, SciPy, matplotlib.

## How to run

```bash
pip install -r requirements.txt
python fetch_data.py      # Boston 2014 finishers -> data/raw/ (gitignored)
python analyze.py         # fits, lookup table and figures -> figures/ and tables/
python export_web.py      # one-minute histograms for the site's chart and lookup -> tables/web_continuum.json
```

## Repo layout

| Path | What it is |
|---|---|
| `fetch_data.py` | Downloads Boston 2014 results and keeps runners only (no wheelchair or handcycle), 2 to 7 hours |
| `analyze.py` | Log-normal fit, record placement, generalized Pareto tail fit, percentile lookup, figures |
| `figures/` | Field distribution with the record, tail fit, percentile curve |
| `export_web.py` | Finish-time histograms by gender and age group, plus the log-normal curve, for the site |
| `tables/` | `summary.csv`, `you_vs_goat.csv`, `web_continuum.json` (chart data) |
| `index.html`, `overview/` | The GitHub Pages site |

## Limitations

Boston is a qualifying race, so this field is faster than a general-entry marathon and every percentile describes this field only; a slower field would put the record further out. The data is one race in one year (2014), since the 2013 race was stopped partway and is left out. The record is set in `analyze.py` as Sabastian Sawe's 1:59:30 (London, 26 April 2026), [ratified by World Athletics](https://worldathletics.org/news/press-releases/ratified-world-records-sawe-ehammer-charlton-mcrae-yan-duplantis-assefa) on 23 July 2026. It replaced Kelvin Kiptum's 2:00:35; the change moved the record mark and the percent-slower figures and none of the field statistics.

## License

[MIT](LICENSE) © 2026 Jeremy Lee. Finisher data from [llimllib/bostonmarathon](https://github.com/llimllib/bostonmarathon).
