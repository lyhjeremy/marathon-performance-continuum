"""
export_web.py - data for the interactive charts on the write-up page.

Reads data/raw/boston_finishers.csv (the file analyze.py reads) and writes
tables/web_continuum.json: one-minute histograms of finish time for the field,
for each gender and for each gender and age group, plus the log-normal curve
from the same fit analyze.py makes. It changes no result.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent
AGES = [(18, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 69), (70, 99)]


def counts(m):
    # bin k holds times in (k, k+1], so "slower than a whole minute" is exact
    return np.histogram(np.ceil(m) - 1, bins=np.arange(120, 422, 1))[0].tolist()


def main():
    df = pd.read_csv(ROOT / "data" / "raw" / "boston_finishers.csv")
    t = df.minutes.values
    floor = 118.0
    shape, loc, scale = stats.lognorm.fit(t - floor, floc=0)   # as in analyze.py
    xs = np.arange(120, 421, 2)
    out = {"source": "data/raw/boston_finishers.csv (Boston 2014, runners only, 120 to 420 min)",
           "start_min": 120, "n": int(len(t)), "median": round(float(np.median(t)), 2), "winner": round(float(t.min()), 2),
           "all": counts(t),
           "lognorm": {"floor": floor, "shape": round(float(shape), 6), "scale": round(float(scale), 6),
                       "x": xs.tolist(), "pdf": [round(float(v), 7) for v in stats.lognorm(shape, loc=floor, scale=scale).pdf(xs)]},
           "groups": {}}
    for g in ["M", "F"]:
        d = df[df.gender == g]
        out["groups"][g] = {"n": int(len(d)), "c": counts(d.minutes.values), "ages": []}
        for lo, hi in AGES:
            a = d[(d.age >= lo) & (d.age <= hi)]
            out["groups"][g]["ages"].append({"lo": lo, "hi": hi, "n": int(len(a)), "c": counts(a.minutes.values)})
    (ROOT / "tables" / "web_continuum.json").write_text(json.dumps(out, separators=(",", ":")))
    # check against tables/you_vs_goat.csv
    for m in [150, 180, 240]:
        print(m, round(100 * (t > m).mean(), 1))
    print(out["n"], out["median"], out["winner"], {g: (v["n"], [a["n"] for a in v["ages"]]) for g, v in out["groups"].items()})


if __name__ == "__main__":
    main()
