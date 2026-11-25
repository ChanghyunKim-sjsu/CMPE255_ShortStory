"""Make slide charts from numbers copied out of the papers.

Run:  python3 figures/make_charts.py
Outputs (1920x1080 PNG, 16:9):
  figures/ablation_igstgnn.png   IGSTGNN Table 5 (arXiv 2602.02528)
  figures/memory_fast_672.png    FaST Table 4 (arXiv 2601.05174)
  figures/metrics_example.png    Illustrative MAE / RMSE / MAPE example (made-up numbers)
"""
import math
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent

# Colors: one highlight hue plus neutrals (single focus, no categorical palette needed).
SURFACE = "#ffffff"
TEXT = "#191919"
TEXT_2 = "#666666"
GRID = "#e6e6e6"
HIGHLIGHT = "#257de0"  # blue
MUTED = "#b5b5b5"      # gray for non-focus bars

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "text.color": TEXT,
    "axes.labelcolor": TEXT_2,
    "xtick.color": TEXT_2,
    "ytick.color": TEXT,
    "axes.edgecolor": GRID,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
})


def style_axes(ax):
    ax.grid(axis="x", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=0)


# ---------------------------------------------------------------- IGSTGNN ablation
# Table 5, average MAE over the 12-step horizon.
ABL = {
    "Alameda": {
        "full": 12.69,
        "w/o ICSF": 13.23, "w/o TIID": 13.23, "w/o sensor attrs": 13.21,
        "w/o distance": 13.20, "w/o incident attrs": 13.09,
    },
    "Contra Costa": {
        "full": 13.43,
        "w/o ICSF": 13.52, "w/o TIID": 13.54, "w/o sensor attrs": 13.52,
        "w/o distance": 13.55, "w/o incident attrs": 13.59,
    },
    "Orange": {
        "full": 13.13,
        "w/o ICSF": 13.38, "w/o TIID": 13.32, "w/o sensor attrs": 13.45,
        "w/o distance": 13.60, "w/o incident attrs": 13.59,
    },
}
VARIANTS = ["w/o ICSF", "w/o TIID", "w/o sensor attrs", "w/o distance", "w/o incident attrs"]


def chart_ablation():
    pct = {
        ds: [(vals[v] / vals["full"] - 1) * 100 for v in VARIANTS]
        for ds, vals in ABL.items()
    }
    lo = min(min(p) for p in pct.values())
    hi = max(max(p) for p in pct.values())
    print(f"IGSTGNN ablation MAE increase range: {lo:.2f}% to {hi:.2f}%")

    fig, axes = plt.subplots(1, 3, figsize=(13.333, 7.5), dpi=144, sharey=True, sharex=True)
    ys = list(range(len(VARIANTS)))[::-1]
    for ax, (ds, vals) in zip(axes, ABL.items()):
        style_axes(ax)
        bars = ax.barh(ys, pct[ds], color=HIGHLIGHT, height=0.55)
        for b, v, p in zip(bars, VARIANTS, pct[ds]):
            ax.text(p + 0.08, b.get_y() + b.get_height() / 2,
                    f"+{p:.1f}%  ({vals[v]:.2f})", va="center", fontsize=12, color=TEXT)
        ax.set_title(f"{ds}\nfull model MAE = {vals['full']:.2f}", fontsize=15, color=TEXT, loc="left")
        ax.set_yticks(ys)
        ax.set_yticklabels(VARIANTS, fontsize=14)
        ax.set_xlim(0, 6.4)
        ax.set_xticks([0, 1, 2, 3, 4, 5])
        ax.set_xticklabels([f"{t}%" for t in [0, 1, 2, 3, 4, 5]], fontsize=12)
    fig.suptitle("IGSTGNN ablation: removing any component raises MAE by 0.7% to 4.3%",
                 x=0.04, ha="left", fontsize=22, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.905, "Bars: MAE increase vs. the full model on each dataset. Labels: increase (MAE of the variant).",
             fontsize=13, color=TEXT_2)
    fig.text(0.04, 0.03, "Source: Fan et al., Incident-Guided Spatiotemporal Traffic Forecasting, KDD 2026, arXiv 2602.02528, Table 5 "
             "(average MAE over the 12-step horizon). Percentages computed by the author.",
             fontsize=10.5, color=TEXT_2)
    fig.subplots_adjust(left=0.13, right=0.98, top=0.78, bottom=0.12, wspace=0.12)
    fig.savefig(OUT / "ablation_igstgnn.png")
    plt.close(fig)


# ---------------------------------------------------------------- FaST memory
# Table 4: GPU memory (GB) for 672-step forecasting. None = out of memory ("/" in the paper).
MEM = {
    "SD (716 nodes)":    {"FaST": 3.7,  "DLinear": 3.2,  "STID": 3.5,  "BigST": 5.7,  "PatchSTG": 8.6,  "GWNet": 34.5, "STGCN": 38.8},
    "GBA (2,352 nodes)": {"FaST": 10.9, "DLinear": 9.2,  "STID": 10.4, "BigST": 17.8, "PatchSTG": 33.9, "GWNet": None, "STGCN": 41.1},
    "GLA (3,834 nodes)": {"FaST": 17.4, "DLinear": 14.7, "STID": 16.6, "BigST": 28.5, "PatchSTG": 32.1, "GWNet": None, "STGCN": None},
    "CA (8,600 nodes)":  {"FaST": 38.1, "DLinear": 32.3, "STID": 36.7, "BigST": 30.9, "PatchSTG": 42.3, "GWNet": None, "STGCN": None},
}
MODELS = ["FaST", "DLinear", "STID", "BigST", "PatchSTG", "GWNet", "STGCN"]
GPU_LIMIT = 48  # RTX A6000


def chart_memory():
    fig, axes = plt.subplots(1, 4, figsize=(13.333, 7.5), dpi=144, sharey=True, sharex=True)
    ys = list(range(len(MODELS)))[::-1]
    for ax, (ds, vals) in zip(axes, MEM.items()):
        style_axes(ax)
        ax.axvline(GPU_LIMIT, color=TEXT_2, linestyle=(0, (4, 3)), linewidth=1.2)
        for y, m in zip(ys, MODELS):
            v = vals[m]
            if v is None:
                ax.text(0.8, y, "out of memory", va="center", fontsize=11, color=TEXT_2, style="italic")
                continue
            color = HIGHLIGHT if m == "FaST" else MUTED
            ax.barh(y, v, color=color, height=0.55)
            ax.text(v + 0.9, y, f"{v:g}", va="center", fontsize=12, color=TEXT,
                    fontweight="bold" if m == "FaST" else "normal", zorder=5,
                    bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5))
        ax.set_title(ds, fontsize=14, color=TEXT, loc="left")
        ax.set_xlim(0, 56)
        ax.set_xticks([0, 12, 24, 36, 48])
        ax.set_xticklabels(["0", "12", "24", "36", "48 GB"], fontsize=11)
        ax.set_yticks(ys)
        ax.set_yticklabels(MODELS, fontsize=14)
    axes[0].get_yticklabels()[0].set_fontweight("bold")
    fig.suptitle("FaST still runs at 8,600 nodes, where GWNet and STGCN run out of memory",
                 x=0.04, ha="left", fontsize=22, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.905, "GPU memory for 672-step forecasting (lower is better). Dashed line: 48 GB GPU limit (RTX A6000). "
             "Gray labels: the model ran out of memory.", fontsize=13, color=TEXT_2)
    fig.text(0.04, 0.03, "Source: Zhao et al., FaST, KDD 2026, arXiv 2601.05174, Table 4. Batch size 64, except GWNet on SD, BigST on CA "
             "and PatchSTG on CA (32).", fontsize=10.5, color=TEXT_2)
    fig.subplots_adjust(left=0.09, right=0.99, top=0.80, bottom=0.12, wspace=0.10)
    fig.savefig(OUT / "memory_fast_672.png")
    plt.close(fig)


# ---------------------------------------------------------------- metrics example
# Illustrative numbers (NOT from the papers): speed errors at 5 sensors, in km/h.
ERR_A = [4, 4, 4, 4, 4]
ERR_B = [1, 1, 1, 1, 16]
ORANGE = "#f47230"  # the one big miss


def mae(e):
    return sum(abs(x) for x in e) / len(e)


def rmse(e):
    return math.sqrt(sum(x * x for x in e) / len(e))


def chart_metrics():
    print(f"Model A: MAE {mae(ERR_A):.1f}, RMSE {rmse(ERR_A):.1f}; "
          f"Model B: MAE {mae(ERR_B):.1f}, RMSE {rmse(ERR_B):.1f}")
    mape_cases = [("true speed 60 km/h", 5 / 60 * 100), ("true speed 5 km/h", 5 / 5 * 100)]
    for n, v in mape_cases:
        print(f"MAPE {n}, abs. error 5: {v:.1f}%")

    fig = plt.figure(figsize=(13.333, 7.5), dpi=144)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1], left=0.07, right=0.97, top=0.80, bottom=0.14,
                          hspace=0.75, wspace=0.28)
    ax_a, ax_b = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0])
    ax_m = fig.add_subplot(gs[:, 1])

    for ax, errs, name in [(ax_a, ERR_A, "Model A: steady errors"), (ax_b, ERR_B, "Model B: one big miss")]:
        ax.grid(axis="y", color=GRID, linewidth=1)
        ax.set_axisbelow(True)
        ax.tick_params(length=0)
        cols = [ORANGE if e == max(errs) and errs is ERR_B else HIGHLIGHT for e in errs]
        ax.bar(range(1, 6), errs, color=cols, width=0.55)
        for i, e in enumerate(errs, start=1):
            ax.text(i, e + 0.6, f"{e}", ha="center", fontsize=13, color=TEXT)
        ax.set_ylim(0, 25)
        ax.set_yticks([0, 8, 16])
        ax.set_xticks(range(1, 6))
        ax.set_xticklabels([f"sensor {i}" for i in range(1, 6)], fontsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.set_title(name, fontsize=15, color=TEXT, loc="left")
        ax.text(5.45, 22.5, f"MAE {mae(errs):.1f}   RMSE {rmse(errs):.1f}", ha="right", va="center",
                fontsize=16, fontweight="bold", color=TEXT)
        ax.spines["bottom"].set_color(GRID)
    ax_a.set_ylabel("absolute error (km/h)", fontsize=12)
    ax_b.set_ylabel("absolute error (km/h)", fontsize=12)

    ax_m.grid(axis="y", color=GRID, linewidth=1)
    ax_m.set_axisbelow(True)
    ax_m.tick_params(length=0)
    vals = [v for _, v in mape_cases]
    ax_m.bar([0, 1], vals, color=[HIGHLIGHT, ORANGE], width=0.5)
    for x, v in zip([0, 1], vals):
        ax_m.text(x, v + 2, f"{v:.0f}%" if v >= 99 else f"{v:.1f}%", ha="center", fontsize=16, fontweight="bold", color=TEXT)
    ax_m.set_xticks([0, 1])
    ax_m.set_xticklabels([f"{n}\nerror 5 km/h" for n, _ in mape_cases], fontsize=13)
    ax_m.set_ylim(0, 118)
    ax_m.set_yticks([0, 25, 50, 75, 100])
    ax_m.set_yticklabels([f"{t}%" for t in [0, 25, 50, 75, 100]], fontsize=12)
    ax_m.set_title("MAPE for the same 5 km/h error", fontsize=15, color=TEXT, loc="left")
    ax_m.spines["bottom"].set_color(GRID)

    fig.suptitle("Same MAE, different RMSE. Same error, very different MAPE.",
                 x=0.04, ha="left", fontsize=22, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.905, "Left: RMSE punishes one big miss. Right: MAPE explodes when the true value is near zero.",
             fontsize=13, color=TEXT_2)
    fig.text(0.04, 0.03, "Illustrative example with made-up numbers (not from the papers). "
             "MAE = mean |error|; RMSE = sqrt(mean error^2); MAPE = mean |error| / |true value|.",
             fontsize=10.5, color=TEXT_2)
    fig.savefig(OUT / "metrics_example.png")
    plt.close(fig)


if __name__ == "__main__":
    chart_ablation()
    chart_memory()
    chart_metrics()
    print("saved to", OUT)
