# The Marathon Performance Continuum

*One distribution from the back of the field to the world record.*

## The question

Runners want to know where their time sits. Fans want to know how fast the world record really is. Both get answered with adjectives. Put on one time axis, they turn into the same question: your time is one point on a curve, and the record is another point on it.

I used the **31,842 finishers of the 2014 Boston Marathon** to draw that curve, then placed the record on it.

## The shape of a field

<p align="center">
  <img src="figures/continuum.png" alt="Histogram of 31,842 Boston 2014 finish times with a log-normal fit; the 2:00:35 world record line sits left of the whole field, including the winner's 2:09." width="760">
</p>

A marathon field is close to **log-normal**. It rises to a peak around 3:30 to 3:50, then trails off slowly past six hours. The median Boston finisher ran **3:52**. The slow tail pulls the mean to **4:03**, with a standard deviation of 51 minutes. A shifted log-normal with a floor at 118 minutes tracks the histogram closely.

Kelvin Kiptum's **2:00:35** is not at the fast end of this distribution. It is to the left of all of it. None of the 31,842 finishers ran faster, and the Boston winner finished in **2:09**. Against this field the record is **2.4 standard deviations below the mean**, and the median runner took **93% longer**.

## Where the fast edge ends

<p align="center">
  <img src="figures/evt_tail.png" alt="Histogram of minutes under the 2:56 threshold for the fastest 5 percent of finishers, with a generalized Pareto curve of shape -0.15." width="720">
</p>

The log-normal describes the middle of the field and says little about its extreme fast end. For that I used **Extreme Value Theory**. I set a threshold at the fastest 5% of finishers (2:56, which leaves 1,593 runners), measured how far each of them beat it, and fitted a **generalized Pareto** distribution to those gaps (Peaks-Over-Threshold).

The fitted shape parameter is **ξ = −0.147**. A negative shape means the tail is **bounded**: fast performances stop at some finite point instead of thinning out forever. The method is good at detecting whether a bound exists and poor at locating it, so I don't quote a fastest possible time.

## Where your time lands

<p align="center">
  <img src="figures/percentile.png" alt="Curve of finish time against the percent of the Boston field finished ahead of, steepest between 3:00 and 4:00." width="720">
</p>

The lookup turns a finish time into a place in the field (`tables/you_vs_goat.csv`):

| Finish time | Ahead of this share of the field | Slower than 2:00:35 by |
|---|---|---|
| 2:30 | 99.7% | 24.4% |
| 3:00 | 92.6% | 49.3% |
| 3:30 | 70.6% | 74.2% |
| 4:00 | 43.2% | 99.0% |
| 5:00 | 14.4% | 148.8% |
| 6:00 | 2.8% | 198.5% |

A 3:00 marathon is a serious amateur result and beats 92.6% of an already fast field. It is still 49% slower than the record. A 4:00 takes almost exactly twice as long as the record.

## Limitations

Boston is a qualifying race, so this is a field of runners who were fast enough to get in, not the general public. Every percentile here is about this field. A general-entry race would shift the whole curve slower and put the record further out.

It is one race in one year. The 2013 race was stopped partway through and is left out.

I don't give the record's rarity as "1 in N", because that would mean trusting the fitted density well beyond the data. The record is described by what was observed instead.

The record is set in `analyze.py` as Kiptum's 2:00:35 (Chicago, 2023). A faster record would move that one mark and none of the field statistics.

*Code: [github.com/lyhjeremy/marathon-performance-continuum](https://github.com/lyhjeremy/marathon-performance-continuum)*
