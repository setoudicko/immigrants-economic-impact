#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 01:34:37 2026

@author: agaichatoudicko
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# 1. LOAD DATA
df = pd.read_csv("Survey for foreign-born residents of Syracuse _2026-04-04.csv")
df = df.rename(columns={
    "What is your gender?":                     "gender",
    "How old are you?":                         "age",
    "What is your educational level?":          "education",
    "What is your English skill proficiency?":  "english_proficiency",
    "After arriving in Syracuse, how long does it take to find a job? ":
                                                "time_to_find_job",
    "How much do you earn as income?":          "income",
    "Approximately what percentage of your income is spent locally (housing, groceries, transportation, services in Syracuse)?":
                                                "pct_income_local",
    "Do you currently volunteer in any community service activities?":
                                                "volunteers"
})

# 2. NUMERIC MAPPINGS
edu_map = {
    "Middle School":  1,
    "High School":    2,
    "Graduate degree": 4
}
# Get exact Bachelor's value
bachelors = [x for x in df["education"].unique() if "achelor" in str(x)][0]
edu_map[bachelors] = 3

eng_map = {"Basic": 1, "Intermediate": 2, "Advanced": 3}

job_map = {
    "Less than 3 months": 1,
    "Six months":         2,
    "One year":           3,
    "Two years":          4,
    "Three years":        5
}

inc_map = {
    "$100 to $500":          1,
    "$500 to $1000":         2,
    "Weekly $500 to $1000":  2,
    "$1000 to $2000":        3,
    "$3000 or more":         4
}

pct_map = {
    "25% or less": 1,
    "26 - 50%":    2,
    "51 - 75%":    3,
    "76 - 100%":   4
}

df["edu_n"] = df["education"].map(edu_map)
df["eng_n"] = df["english_proficiency"].map(eng_map)
df["job_n"] = df["time_to_find_job"].map(job_map)
df["inc_n"] = df["income"].map(inc_map)
df["pct_n"] = df["pct_income_local"].map(pct_map)

# 3. Variable Correlation Matrix
vars_for_corr = ["edu_n", "eng_n", "inc_n", "pct_n"]
labels_corr = [
    "Education",
    "English\nProficiency",
    "Income",
    "% Spent\nLocally"
]

df_corr = df[vars_for_corr].dropna()
corr_matrix = df_corr.corr()

print("4-Variable Correlation Matrix:")
print(corr_matrix.round(3))

fig_corr, ax_corr = plt.subplots(figsize=(9, 7))
sns.heatmap(corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="RdBu_r",
            center=0,
            linewidths=0.8,
            ax=ax_corr,
            annot_kws={"size": 14, "weight": "bold"},
            xticklabels=labels_corr,
            yticklabels=labels_corr,
            vmin=-1, vmax=1)

ax_corr.set_title(
    "Figure 17 . Correlation Matrix — Key Economic Variables (n=30)",
    fontsize=14, fontweight="bold", pad=15
)
ax_corr.tick_params(axis="both", labelsize=12)

plt.tight_layout()
plt.savefig("fig17_correlation_matrix.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig17_correlation_matrix.png")


fig_path, ax_path = plt.subplots(figsize=(18, 12))
ax_path.set_xlim(0, 10)
ax_path.set_ylim(0, 7)
ax_path.axis("off")
ax_path.set_facecolor("#f8f9fa")

# Node positions
nodes = {
    "Education":         (1.8, 3.5),
    "English\nProficiency": (5.0, 6.0),
    "Income":            (5.0, 1.0),
    "% Spent\nLocally":  (8.5, 3.5)
}

node_colors = {
    "Education":         "#3498db",
    "English\nProficiency": "#2ecc71",
    "Income":            "#e74c3c",
    "% Spent\nLocally":  "#9b59b6"
}

node_radius = 0.75

# ── Draw nodes ────────────────────────────────────────────────────────────────
for name, (x, y) in nodes.items():
    # Shadow
    shadow = plt.Circle((x+0.06, y-0.06), node_radius,
                         color="gray", alpha=0.2, zorder=2)
    ax_path.add_patch(shadow)
    # Main circle
    circle = plt.Circle((x, y), node_radius,
                         color=node_colors[name],
                         zorder=3, alpha=0.92)
    ax_path.add_patch(circle)
    # White border
    border = plt.Circle((x, y), node_radius,
                         fill=False,
                         edgecolor="white",
                         linewidth=2.5,
                         zorder=4)
    ax_path.add_patch(border)
    # Label
    ax_path.text(x, y, name,
                ha="center", va="center",
                fontsize=12, fontweight="bold",
                color="white", zorder=5)

# ── Arrow and label helper ────────────────────────────────────────────────────
def draw_arrow(ax, start, end, r_val, color, curve=0.0, label_offset=(0, 0)):
    x1, y1 = nodes[start]
    x2, y2 = nodes[end]

    # Adjust start and end to circle edge
    dx = x2 - x1
    dy = y2 - y1
    dist = np.sqrt(dx**2 + dy**2)
    ux = dx / dist
    uy = dy / dist

    xs = x1 + ux * node_radius
    ys = y1 + uy * node_radius
    xe = x2 - ux * node_radius
    ye = y2 - uy * node_radius

    ax.annotate("",
        xy=(xe, ye),
        xytext=(xs, ys),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=2.8,
            mutation_scale=18,
            connectionstyle=f"arc3,rad={curve}"
        ),
        zorder=6
    )

    # Label midpoint
    mx = (xs + xe) / 2 + label_offset[0]
    my = (ys + ye) / 2 + label_offset[1]

    ax.text(mx, my, f"r = {r_val}",
            ha="center", va="center",
            fontsize=11, fontweight="bold",
            color=color,
            bbox=dict(
                boxstyle="round,pad=0.35",
                facecolor="white",
                edgecolor=color,
                alpha=0.95,
                linewidth=1.8
            ),
            zorder=7)

# ── Draw all paths from correlation matrix ────────────────────────────────────

# Education → English Proficiency (r=0.33) — strongest
draw_arrow(ax_path,
           "Education", "English\nProficiency",
           r_val=0.33,
           color="#2ecc71",
           curve=0.1,
           label_offset=(-0.5, 0.3))

# Education → Income (r=0.31)
draw_arrow(ax_path,
           "Education", "Income",
           r_val=0.31,
           color="#e74c3c",
           curve=-0.1,
           label_offset=(-0.5, -0.3))

# Education → % Spent Locally (r=0.26)
draw_arrow(ax_path,
           "Education", "% Spent\nLocally",
           r_val=0.26,
           color="#3498db",
           curve=0.0,
           label_offset=(0.0, 0.4))

# English → Income (r=0.17)
draw_arrow(ax_path,
           "English\nProficiency", "Income",
           r_val=0.17,
           color="#2ecc71",
           curve=0.1,
           label_offset=(0.5, 0.0))

# English → % Spent Locally (r=0.13) — weakest
draw_arrow(ax_path,
           "English\nProficiency", "% Spent\nLocally",
           r_val=0.13,
           color="#2ecc71",
           curve=0.1,
           label_offset=(0.0, 0.4))

# Income → % Spent Locally (r=0.25)
draw_arrow(ax_path,
           "Income", "% Spent\nLocally",
           r_val=0.25,
           color="#e74c3c",
           curve=-0.1,
           label_offset=(0.5, -0.3))

# Legend
legend_elements = [
    mpatches.Patch(color="#3498db", label="Education"),
    mpatches.Patch(color="#2ecc71", label="English Proficiency"),
    mpatches.Patch(color="#e74c3c", label="Income"),
    mpatches.Patch(color="#9b59b6", label="% Spent Locally"),
]
ax_path.legend(
    handles=legend_elements,
    loc="lower left",
    fontsize=11,
    framealpha=0.95,
    edgecolor="gray",
    title="Variables",
    title_fontsize=12
)

#Strength guide 
ax_path.text(9.8, 0.3,
    "Correlation Strength:\nr ≥ 0.40 = Moderate\nr 0.20–0.39 = Weak\nr < 0.20 = Very Weak",
    ha="right", va="bottom",
    fontsize=9, color="#555555",
    bbox=dict(boxstyle="round,pad=0.4",
              facecolor="white",
              edgecolor="gray",
              alpha=0.9))

# ── Title ─────────────────────────────────────────────────────────────────────
ax_path.set_title(
    "Figure 18 · Path Analysis — Economic Integration of "
    "Foreign-Born Residents in Syracuse (n=30)\n"
    "All paths are positive — no paths reached statistical "
    "significance (p>.05)",
    fontsize=13,
    fontweight="bold",
    pad=20,
    color="#2c3e50"
)

plt.tight_layout()
plt.savefig("fig18_path_diagram.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig18_path_diagram.png")
