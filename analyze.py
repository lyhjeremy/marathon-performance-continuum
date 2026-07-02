"""The marathon performance continuum — from the back of the field to the GOAT.

We model the distribution of a full marathon field and ask where any performance
falls on it, then quantify just how far the world record sits beyond the human
crowd — using both the fitted body distribution and Extreme Value Theory on the
fast tail.

1. Fit a (shifted) log-normal to the finish-time distribution.
2. Locate the world record (2:00:35) on that distribution: percentile, z-score,
   and a "1-in-N of this field" rarity.
3. Peaks-Over-Threshold EVT (Generalized Pareto) on the fast tail to characterise
   how the elite edge behaves and estimate its endpoint.
4. A percentile / "you-vs-GOAT" lookup.

Outputs: figures/*.png and tables/*.csv
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent
FIG, TAB = ROOT / "figures", ROOT / "tables"
WR_MIN = 120.5833          # men's marathon WR 2:00:35 (Kelvin Kiptum, 2023)
WR_LABEL = "2:00:35"
INK, GOLD, WINE, SKY = "#1a1a2e", "#D4A537", "#7a1f2b", "#4a7ba6"


def hhmm(m: float) -> str:
    h, mm = divmod(int(round(m)), 60)
    return f"{h}:{mm:02d}"


def main() -> None:
    FIG.mkdir(exist_ok=True); TAB.mkdir(exist_ok=True)
    df = pd.read_csv(ROOT / "data" / "raw" / "boston_finishers.csv")
    t = df.minutes.values
    n = len(t)
    print(f"field: {n:,} finishers  median {hhmm(np.median(t))}  "
          f"mean {hhmm(t.mean())}  fastest {hhmm(t.min())}")

    # 1. shifted log-normal fit (floor = a plausible human ceiling, 118 min)
    floor = 118.0
    shape, loc, scale = stats.lognorm.fit(t - floor, floc=0)
    ln = stats.lognorm(shape, loc=floor, scale=scale)

    # 2. world-record position on the field (empirical + robust; the fitted extreme
    #    tail CDF is not trustworthy this far out, so we don't quote a "1-in-N".)
    faster = int((t < WR_MIN).sum())
    z = (WR_MIN - t.mean()) / t.std()
    med_slower = 100 * (np.median(t) - WR_MIN) / WR_MIN
    print(f"\nWorld record {WR_LABEL}:")
    print(f"  faster than ALL {n:,} finishers — including the winner ({faster} were faster)")
    print(f"  {abs(z):.1f} standard deviations below the field mean")
    print(f"  the median finisher ({hhmm(np.median(t))}) is {med_slower:.0f}% slower than the WR")

    # 3. EVT — Peaks-Over-Threshold on the fast tail. The GPD *shape* ξ is the robust
    #    output (is the edge bounded or heavy?); the point endpoint is deliberately
    #    NOT reported — POT endpoint estimates are notoriously unstable.
    u = np.percentile(t, 5)                       # fastest 5% threshold
    exceed = u - t[t < u]                          # how far under the threshold (positive)
    c, gloc, gscale = stats.genpareto.fit(exceed, floc=0)
    print(f"\nEVT fast tail (threshold {hhmm(u)}, {len(exceed)} performances):")
    print(f"  GPD shape ξ = {c:+.3f}  → {'bounded: a finite fast edge, not a heavy tail' if c < 0 else 'unbounded/heavy'}")

    # 4. percentile / you-vs-GOAT table
    refs = [125, 150, 165, 180, 210, 240, 270, 300, 360]
    rows = [{"time": hhmm(m), "minutes": m,
             "field_percentile": round(100 * (t > m).mean(), 1),
             "pct_slower_than_WR": round(100 * (m - WR_MIN) / WR_MIN, 1)} for m in refs]
    pd.DataFrame(rows).to_csv(TAB / "you_vs_goat.csv", index=False)
    pd.DataFrame([{"n": n, "median_min": np.median(t), "mean_min": t.mean(),
                   "sd_min": t.std(), "wr_min": WR_MIN, "wr_z": z,
                   "n_faster_than_wr": faster, "gpd_shape": c}]
                 ).to_csv(TAB / "summary.csv", index=False)

    _figures(t, df, ln, u, exceed, c, gscale)


def _figures(t, df, ln, u, exceed, c, gscale):
    # Fig 1: the continuum — where everyone (and the GOAT) falls
    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.hist(t, bins=90, color="#d9d2c4", edgecolor="white", linewidth=0.3, density=True)
    xs = np.linspace(t.min(), t.max(), 400)
    ax.plot(xs, ln.pdf(xs), color=WINE, lw=2, label="log-normal fit")
    for val, lab, col in [(np.median(t), "field median", INK), (t.min(), "Boston winner", SKY)]:
        ax.axvline(val, color=col, ls="--", lw=1.3)
        ax.text(val, ax.get_ylim()[1]*0.92, f" {lab}\n {hhmm(val)}", fontsize=8, color=col)
    ax.axvline(WR_MIN, color=GOLD, ls="-", lw=2)
    ax.text(WR_MIN - 3, ax.get_ylim()[1]*0.6, f"World record\n{WR_LABEL}", fontsize=9,
            color="#a67c00", ha="right", fontweight="bold")
    ax.set_xlabel("finish time (h:mm)")
    ax.set_ylabel("density of finishers")
    ax.set_xticks(range(120, 421, 30)); ax.set_xticklabels([hhmm(m) for m in range(120, 421, 30)])
    ax.set_title("The marathon continuum: 32,000 Boston finishers — and the GOAT far to the left",
                 fontweight="bold", fontsize=12)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "continuum.png", dpi=150); plt.close(fig)

    # Fig 2: EVT tail fit (fast edge)
    fig, ax = plt.subplots(figsize=(8.5, 5))
    fast = t[t < u]
    ax.hist(u - fast, bins=40, color="#d9d2c4", edgecolor="white", density=True, label="exceedances (min under threshold)")
    ex = np.linspace(0, exceed.max(), 300)
    ax.plot(ex, stats.genpareto.pdf(ex, c, 0, gscale), color=WINE, lw=2,
            label=f"Generalized Pareto (ξ={c:+.2f})")
    ax.set_xlabel(f"minutes faster than the {hhmm(u)} threshold (fast 5% of field)")
    ax.set_ylabel("density")
    edge = "bounded — a finite fast edge" if c < 0 else "heavy/unbounded"
    ax.set_title(f"Extreme Value Theory on the elite tail: {edge} (ξ = {c:+.2f})", fontweight="bold")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "evt_tail.png", dpi=150); plt.close(fig)

    # Fig 3: you-vs-GOAT percentile curve
    fig, ax = plt.subplots(figsize=(8.5, 5))
    grid = np.linspace(t.min(), np.percentile(t, 99.5), 300)
    pct = [100 * (t > m).mean() for m in grid]      # % of field you'd beat
    ax.plot(grid, pct, color=WINE, lw=2.2)
    for m in [150, 180, 210, 240, 300]:
        p = 100 * (t > m).mean()
        ax.scatter([m], [p], color=GOLD, zorder=5)
        ax.text(m, p + 2, f"{hhmm(m)}\ntop {100-p:.0f}%", fontsize=7.5, ha="center", color=INK)
    ax.set_xlabel("your finish time (h:mm)")
    ax.set_ylabel("% of the Boston field you finish ahead of")
    ax.set_xticks(range(120, 361, 30)); ax.set_xticklabels([hhmm(m) for m in range(120, 361, 30)])
    ax.set_title("You vs the field: where any marathon time ranks", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "percentile.png", dpi=150); plt.close(fig)
    print(f"\nwrote {len(list(FIG.glob('*.png')))} figures and {len(list(TAB.glob('*.csv')))} tables")


# make hhmm available inside _figures
globals()["hhmm"] = hhmm
if __name__ == "__main__":
    main()
