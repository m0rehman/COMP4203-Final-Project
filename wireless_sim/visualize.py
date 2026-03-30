# visualize.py
# helper for main.py — receives simulation results and writes results.png.
# not intended to be run standalone.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BUFFER_MAX = 50

COLOURS = {
    "Standard AP":   "#ff0800",
    "MAC Filter AP": "#2b00ff",
    "Adaptive AP":   "#00ff00",
}
AP_LABELS = ["Standard AP", "MAC Filter AP", "Adaptive AP"]


def metrics_list(raw):
    total   = raw.get("total_packets", 0)
    recv    = raw.get("received", 0)
    blocked = raw.get("blocked_auths", 0)
    collide = raw.get("collisions", 0)
    buf     = raw.get("buffer_usage", 0)
    denom   = recv + blocked
    return {
        "auth_pass_pct":   (recv / denom * 100) if denom else 100.0,
        "collision_pct":   (collide / total * 100) if total else 0.0,
        "buffer_fill_pct": (buf / BUFFER_MAX * 100),
        "detection_lat":   raw.get("detection_latency_ms"),
        "mcs_increases":   raw.get("mcs_increases"),
    }


def get_metric(results, scenario, ap_label, key, fallback=0):
    for ap, raw in results[scenario]:
        if ap == ap_label:
            v = metrics_list(raw).get(key)
            return v if v is not None else fallback
    return fallback


def plot(results, out="results.png"):
    scenarios = list(results.keys())
    x = np.arange(len(scenarios))
    bw = 0.25

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("AP Performance Comparison", fontsize=14, fontweight="bold")

    subplots = [
        (axes[0, 0], "auth_pass_pct", "Authentication Pass Rate (%)", "Pass Rate (%)"),
        (axes[0, 1], "collision_pct", "Collision Rate (%)", "Collision Rate (%)"),
        (axes[1, 0], "buffer_fill_pct", "Auth Buffer Fill (%)", "Buffer Fill (%)"),
        (axes[1, 1], None, "DoS Detection Latency (ms)", "Latency (ms)"),
    ]

    for ax, key, title, ylabel in subplots:
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(scenarios, fontsize=8)

        if key is not None:
            for i, ap in enumerate(AP_LABELS):
                vals = [get_metric(results, s, ap, key) for s in scenarios]
                ax.bar(x + (i - 1) * bw, vals, bw * 0.9, label=ap, color=COLOURS[ap])
            if key == "buffer_fill_pct":
                ax.axhline(100, color="red", linestyle="--", label="buffer full")
                ax.text(x[-1] + 0.5, 101, "buffer full", color="red", fontsize=12, va="bottom")
        else:
            for i, ap in enumerate(AP_LABELS):
                vals     = [get_metric(results, s, ap, "detection_lat", None) for s in scenarios]
                bar_vals = [v if v is not None else 0 for v in vals]
                bars = ax.bar(x + (i - 1) * bw, bar_vals, bw * 0.9, label=ap, color=COLOURS[ap])
                for bar, raw_val in zip(bars, vals):
                    if raw_val is None:
                        ax.text(bar.get_x() + bar.get_width() / 2, 10,
                                "N/A", ha="center", va="bottom", fontsize=7, color="gray")

    handles = [plt.Rectangle((0, 0), 1, 1, color=COLOURS[ap]) for ap in AP_LABELS]
    fig.legend(handles, AP_LABELS, loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.01))

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nResults saved as: {out}")