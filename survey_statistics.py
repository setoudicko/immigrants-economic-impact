#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:18:11 2026

@author: agaichatoudicko
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data
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

# 2. Numeric mappings
age_map_n = {
    '18-24': 21, '25-34': 29.5,
    '35-49': 42, '50 +':  55,
    '15 +':  15
}
edu_map_n = {
    'Middle School':  1,
    'High School':    2,
    "Bachelor's":     3,
    'Graduate degree': 4
}
eng_map_n = {
    'Basic':        1,
    'Intermediate': 2,
    'Advanced':     3
}
inc_map_n = {
    '$100 to $500':          300,
    '$500 to $1000':         750,
    '$1000 to $2000':       1500,
    '$3000 or more':        3000,
    'Weekly $500 to $1000':  750
}
job_map_n = {
    'Less than 3 months': 1,
    'Six months':         2,
    'One year':           3,
    'Two years':          4,
    'Three years':        5
}
pct_map_n = {
    '25% or less': 12.5,
    '26 - 50%':    38.0,
    '51 - 75%':    63.0,
    '76 - 100%':   88.0
}

df["age_n"] = df["age"].map(age_map_n)
df["edu_n"] = df["education"].map(edu_map_n).fillna(3)
df["eng_n"] = df["english_proficiency"].map(eng_map_n)
df["inc_n"] = df["income"].map(inc_map_n)
df["job_n"] = df["time_to_find_job"].map(job_map_n)
df["pct_n"] = df["pct_income_local"].map(pct_map_n)

# 3. Print summary table
variables = {
    "Age (midpoint)":         "age_n",
    "Education Level":        "edu_n",
    "English Proficiency":    "eng_n",
    "Income ($)":             "inc_n",
    "Time to Find Job":       "job_n",
    "% Income Spent Locally": "pct_n"
}

print(f"\n{'Variable':<25} {'n':>5} {'Mean':>10} {'Median':>10} "
      f"{'Std Dev':>10} {'Min':>10} {'Max':>10}")
print("-" * 80)
for label, col in variables.items():
    s = df[col].dropna()
    print(f"{label:<25} {len(s):>5} {s.mean():>10.2f} "
          f"{s.median():>10.2f} {s.std():>10.2f} "
          f"{s.min():>10.2f} {s.max():>10.2f}")

# 4. FIG 16 · Statistical summary
fig16, axes = plt.subplots(2, 3, figsize=(30, 18))
fig16.suptitle(
    "Fig 16 · Statistical Summary of Survey Respondents (n=30)",
    fontsize=26, fontweight="bold", y=1.01
)

for ax, (label, col) in zip(axes.flatten(), variables.items()):
    s      = df[col].dropna()
    mean   = s.mean()
    median = s.median()
    std    = s.std()

    # Histogram
    ax.hist(s, bins=8, color="#3498db",
            edgecolor="white", alpha=0.75, linewidth=1.2)

    # Mean line
    ax.axvline(mean, color="#e74c3c", linewidth=4,
               linestyle="--", label=f"Mean: {mean:.2f}")

    # Median line
    ax.axvline(median, color="#2ecc71", linewidth=4,
               linestyle="-", label=f"Median: {median:.2f}")

    # Std Dev shading
    ax.axvspan(mean - std, mean + std, alpha=0.18,
               color="#e74c3c", label=f"±1 SD: {std:.2f}")

    # Variable name
    ax.set_title(label, fontsize=20, fontweight="bold", pad=15)

    # Axis labels
    ax.set_xlabel("Value",  fontsize=16, fontweight="bold")
    ax.set_ylabel("Count",  fontsize=16, fontweight="bold")

    # Tick labels
    ax.tick_params(axis="both", labelsize=15)

    # Legend
    legend = ax.legend(fontsize=14, loc="upper left",
                       framealpha=0.95, edgecolor="black",
                       fancybox=True, borderpad=1,
                       labelspacing=1)
    legend.get_frame().set_linewidth(1.5)

    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)

plt.tight_layout(pad=4.0)
plt.savefig("fig16_stats_summary.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig16_stats_summary.png")

