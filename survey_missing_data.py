#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:08:42 2026

@author: agaichatoudicko
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load data
df = pd.read_csv("Survey for foreign-born residents of Syracuse _2026-04-04.csv")

df = df.rename(columns={
    "What is your gender?":                     "gender",
    "Were you born in the U.S?":                "us_born",
    "What is your marital status?":             "marital_status",
    "Do you have children?":                    "has_children",
    "If yes, how many children do you have?":   "num_children",
    "How old are you?":                         "age",
    "What is your country of origin?":          "country_of_origin",
    "What is your educational level?":          "education",
    "What is your English skill proficiency?":  "english_proficiency",
    "When did you arrive in Syracuse?":         "arrival_year",
    "What is your profession?":                 "profession",
    "After arriving in Syracuse, how long does it take to find a job? ":
                                                "time_to_find_job",
    "What is the frequency of your income payment?":
                                                "income_frequency",
    "How much do you earn as income?":          "income",
    "Approximately what percentage of your income is spent locally (housing, groceries, transportation, services in Syracuse)?":
                                                "pct_income_local",
    "Do you currently volunteer in any community service activities?":
                                                "volunteers",
    "If yes, please specify:":                  "volunteer_details"
})

# 2. Missing data
# Only meaningful variables — exclude Username and Total score
miss_vars      = [
    "Born in the US",
    "Number of Children",
    "Income",
    "% Income Spent Locally"
]
missing_counts = [4, 4, 1, 1]
present_counts = [30 - m for m in missing_counts]

# 3. FIG 2 · Missing data
fig2, axes = plt.subplots(1, 2, figsize=(18, 8))
fig2.suptitle(
    "Fig 2 · Missing Data Summary — Survey Respondents (n=30)",
    fontsize=18, fontweight="bold"
)

# Left chart: Present vs Missing stacked bar
x = range(len(miss_vars))
axes[0].bar(x, present_counts, label="Present",
            color="#2ecc71", edgecolor="white", linewidth=0.8)
axes[0].bar(x, missing_counts, bottom=present_counts,
            label="Missing", color="#e74c3c",
            edgecolor="white", linewidth=0.8)

# Add labels inside bars
for i, (p, m) in enumerate(zip(present_counts, missing_counts)):
    # Present label
    axes[0].text(i, p / 2,
                 f"{p}\n({p/30*100:.0f}%)",
                 ha="center", va="center",
                 fontsize=13, fontweight="bold", color="white")
    # Missing label
    if m > 0:
        axes[0].text(i, p + m / 2,
                     f"{m}\n({m/30*100:.0f}%)",
                     ha="center", va="center",
                     fontsize=13, fontweight="bold", color="white")

axes[0].set_xticks(x)
axes[0].set_xticklabels(miss_vars, rotation=15,
                         ha="right", fontsize=13)
axes[0].set(title="Present vs Missing by Variable",
            ylabel="Number of Respondents",
            ylim=(0, 35))
axes[0].title.set_fontsize(15)
axes[0].title.set_fontweight("bold")
axes[0].yaxis.label.set_fontsize(13)
axes[0].legend(fontsize=12, loc="upper right")
axes[0].spines[["top", "right"]].set_visible(False)

# Right chart: % Missing horizontal bar
miss_pct  = [m / 30 * 100 for m in missing_counts]
colors_m  = ["#e74c3c" if p > 10 else "#f39c12" if p > 3 else "#2ecc71"
             for p in miss_pct]

bars = axes[1].barh(miss_vars, miss_pct, color=colors_m,
                    edgecolor="white", linewidth=0.8)

for bar, pct, cnt in zip(bars, miss_pct, missing_counts):
    axes[1].text(pct + 0.3,
                 bar.get_y() + bar.get_height() / 2,
                 f"{cnt} missing ({pct:.0f}%)",
                 va="center", fontsize=13, fontweight="bold")

axes[1].set_xlim(0, 25)
axes[1].axvline(10, color="gray", linewidth=1.5,
                linestyle="--", label="10% threshold")
axes[1].set(title="% Missing per Variable",
            xlabel="% Missing", ylabel="")
axes[1].title.set_fontsize(15)
axes[1].title.set_fontweight("bold")
axes[1].xaxis.label.set_fontsize(13)
axes[1].tick_params(axis="both", labelsize=13)
axes[1].legend(fontsize=12)
axes[1].spines[["top", "right"]].set_visible(False)

# Add interpretation note
fig2.text(
    0.5, -0.02,
    "Note: All missing rates are below 15% which is acceptable "
    "in survey research. Missing values were excluded from "
    "relevant calculations.",
    ha="center", fontsize=11, style="italic", color="gray"
)

plt.tight_layout(pad=3.0)
plt.savefig("fig2_missing_data.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig2_missing_data.png")