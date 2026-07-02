"""Download Boston Marathon finisher data (the mass-participation field).

Source: llimllib/bostonmarathon on GitHub — official finish times for the full
field. We use it as the "continuum" of committed marathoners: from the back of the
pack to the elite line, against which the world record is a distant outlier.

Boston is a *qualifying* race, so this is the distribution of already-fast,
committed runners — not the general public. We say so plainly in the write-up; it
is still the cleanest large, public marathon field available.

Output: data/raw/boston_finishers.csv  (year, gender, age, minutes)

Usage:  python fetch_data.py
"""

from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import urllib.request

RAW = Path(__file__).resolve().parent / "data" / "raw"
# 2014 is the cleanest full field in the mirror. (2013's race was halted partway,
# truncating the field toward faster finishers, so we leave it out.)
YEARS = [2014]
URL = "https://raw.githubusercontent.com/llimllib/bostonmarathon/master/results/{y}/results.csv"


def _load(year: int) -> pd.DataFrame:
    raw = urllib.request.urlopen(URL.format(y=year), timeout=90).read().decode("utf-8", "replace")
    df = pd.read_csv(io.StringIO(raw))
    df["minutes"] = pd.to_numeric(df.get("official"), errors="coerce")
    df["age"] = pd.to_numeric(df.get("age"), errors="coerce")
    # Runners only: drop wheelchair/handcycle (bib starts with W/H) and implausible times.
    bib = df.get("bib", pd.Series([""] * len(df))).astype(str)
    keep = (~bib.str.upper().str.match(r"^[WH]")) & df["minutes"].between(120, 420) & df["gender"].isin(["M", "F"])
    out = df.loc[keep, ["gender", "age", "minutes"]].copy()
    out.insert(0, "year", year)
    return out


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    frames = []
    for y in YEARS:
        try:
            d = _load(y)
            frames.append(d)
            print(f"  {y}: {len(d):,} finishers  (median {d.minutes.median():.1f} min)")
        except Exception as e:
            print(f"  ! {y}: {type(e).__name__} {e}")
    out = pd.concat(frames, ignore_index=True)
    out.to_csv(RAW / "boston_finishers.csv", index=False)
    print(f"\nwrote data/raw/boston_finishers.csv  ({len(out):,} finishers across {out.year.nunique()} years)")


if __name__ == "__main__":
    main()
