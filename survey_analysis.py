#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:44:05 2026

@author: agaichatoudicko
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# 1. Load Data
df = pd.read_csv("Survey for foreign-born residents of Syracuse _2026-04-04.csv")

# 2. Rename columns
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

# 3. Clean Data
df["country_of_origin"] = df["country_of_origin"].str.strip()

# 4. Label mappings
edu_map = {
    1.0: "Middle School",
    2.0: "High School",
    3.0: "Bachelor's",
    4.0: "Graduate degree"
}
eng_map = {
    1.0: "Basic",
    2.0: "Intermediate",
    3.0: "Advanced"
}
inc_map = {
    300.0:  "$100-500",
    750.0:  "$500-1k",
    1500.0: "$1k-2k",
    3000.0: "$3k+"
}
job_map = {
    1.0: "< 3 months",
    2.0: "6 months",
    3.0: "1 year",
    4.0: "2 years",
    5.0: "3 years"
}
pct_map = {
    1.0: "≤ 25%",
    2.0: "26-50%",
    3.0: "51-75%",
    4.0: "76-100%"
}

df["edu_label"] = df["education"].map(edu_map).fillna("Bachelor's")
df["eng_label"] = df["english_proficiency"].map(eng_map)
df["inc_label"] = df["income"].map(inc_map)
df["job_label"] = df["time_to_find_job"].map(job_map)
df["pct_label"] = df["pct_income_local"].map(pct_map)

# 5. Order lists
age_order = ["18-24", "25-34", "35-49", "50 +"]
edu_order = ["Middle School", "High School", "Bachelor's", "Graduate degree"]
eng_order = ["Basic", "Intermediate", "Advanced"]
inc_order = ["$100-500", "$500-1k", "$1k-2k", "$3k+"]
job_order = ["< 3 months", "6 months", "1 year", "2 years", "3 years"]
pct_order = ["≤ 25%", "26-50%", "51-75%", "76-100%"]
arr_order = ["< 1 year", "1 year", "2 years", "3 years", "4 years",
             "7 years", "9 years", "12 years", "15 years",
             "17 years", "18 years", "20 years", "20+ years"]

# 6. Helper Function
def bar_labels(ax, bars, values, horizontal=False, fontsize=12):
    """Add count labels to bars"""
    for bar, val in zip(bars, values):
        if horizontal:
            ax.text(bar.get_width() + 0.1,
                    bar.get_y() + bar.get_height() / 2,
                    str(val), va="center",
                    fontsize=fontsize, fontweight="bold")
        else:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.1,
                    str(val), ha="center",
                    fontsize=fontsize, fontweight="bold")

# FIG 3 · DEMOGRAPHICS

fig3, axes = plt.subplots(2, 3, figsize=(26, 16))
fig3.suptitle("Fig 3 · Demographic Profile of Survey Respondents (n=30)",
              fontsize=22, fontweight="bold", y=1.01)

# Gender
gender_counts = df["gender"].value_counts()
bars = axes[0, 0].bar(gender_counts.index, gender_counts.values,
                       color=["#3498db", "#e74c3c"],
                       edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, gender_counts.values):
    axes[0, 0].text(bar.get_x() + bar.get_width() / 2,
                    val + 0.2, f"{val}\n({val/30*100:.0f}%)",
                    ha="center", fontsize=12, fontweight="bold")
axes[0, 0].set(title="Gender", ylabel="Count")
axes[0, 0].set_ylim(0, gender_counts.max() + 4)
axes[0, 0].title.set_fontsize(16)
axes[0, 0].title.set_fontweight("bold")
axes[0, 0].tick_params(axis="both", labelsize=13)
axes[0, 0].spines[["top", "right"]].set_visible(False)

# Age
age_counts = df["age"].value_counts().reindex(
    [a for a in age_order if a in df["age"].values])
bars = axes[0, 1].bar(age_counts.index, age_counts.values,
                       color=sns.color_palette("Blues_d", len(age_counts)),
                       edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, age_counts.values):
    axes[0, 1].text(bar.get_x() + bar.get_width() / 2,
                    val + 0.2, f"{val}\n({val/30*100:.0f}%)",
                    ha="center", fontsize=12, fontweight="bold")
axes[0, 1].set(title="Age Group", ylabel="Count")
axes[0, 1].set_ylim(0, age_counts.max() + 4)
axes[0, 1].title.set_fontsize(16)
axes[0, 1].title.set_fontweight("bold")
axes[0, 1].tick_params(axis="both", labelsize=13)
axes[0, 1].spines[["top", "right"]].set_visible(False)

# Marital Status
marital_counts = df["marital_status"].value_counts()
bars = axes[0, 2].bar(marital_counts.index, marital_counts.values,
                       color=sns.color_palette("Set2", len(marital_counts)),
                       edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, marital_counts.values):
    axes[0, 2].text(bar.get_x() + bar.get_width() / 2,
                    val + 0.2, f"{val}\n({val/30*100:.0f}%)",
                    ha="center", fontsize=12, fontweight="bold")
axes[0, 2].set(title="Marital Status", ylabel="Count")
axes[0, 2].set_ylim(0, marital_counts.max() + 4)
axes[0, 2].title.set_fontsize(16)
axes[0, 2].title.set_fontweight("bold")
axes[0, 2].tick_params(axis="both", labelsize=13)
axes[0, 2].spines[["top", "right"]].set_visible(False)

# Has Children
children_counts = df["has_children"].value_counts()
bars = axes[1, 0].bar(children_counts.index, children_counts.values,
                       color=["#9b59b6", "#95a5a6"],
                       edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, children_counts.values):
    axes[1, 0].text(bar.get_x() + bar.get_width() / 2,
                    val + 0.2, f"{val}\n({val/30*100:.0f}%)",
                    ha="center", fontsize=12, fontweight="bold")
axes[1, 0].set(title="Has Children?", ylabel="Count")
axes[1, 0].set_ylim(0, children_counts.max() + 4)
axes[1, 0].title.set_fontsize(16)
axes[1, 0].title.set_fontweight("bold")
axes[1, 0].tick_params(axis="both", labelsize=13)
axes[1, 0].spines[["top", "right"]].set_visible(False)

# Number of Children
num_children_counts = df["num_children"].value_counts()
bars = axes[1, 1].barh(num_children_counts.index,
                        num_children_counts.values,
                        color=sns.color_palette("muted",
                                                len(num_children_counts)),
                        edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, num_children_counts.values):
    axes[1, 1].text(bar.get_width() + 0.1,
                    bar.get_y() + bar.get_height() / 2,
                    f"{val} ({val/30*100:.0f}%)",
                    va="center", fontsize=12, fontweight="bold")
axes[1, 1].set_xlim(0, num_children_counts.max() + 3)
axes[1, 1].set(title="Number of Children", ylabel="", xlabel="Count")
axes[1, 1].title.set_fontsize(16)
axes[1, 1].title.set_fontweight("bold")
axes[1, 1].tick_params(axis="both", labelsize=13)
axes[1, 1].spines[["top", "right"]].set_visible(False)

# Born in US
us_counts = df["us_born"].value_counts()
bars = axes[1, 2].bar(us_counts.index, us_counts.values,
                       color=["#e74c3c", "#2ecc71"],
                       edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, us_counts.values):
    axes[1, 2].text(bar.get_x() + bar.get_width() / 2,
                    val + 0.2, f"{val}\n({val/30*100:.0f}%)",
                    ha="center", fontsize=12, fontweight="bold")
axes[1, 2].set(title="Born in the U.S.?", ylabel="Count")
axes[1, 2].set_ylim(0, us_counts.max() + 4)
axes[1, 2].title.set_fontsize(16)
axes[1, 2].title.set_fontweight("bold")
axes[1, 2].tick_params(axis="both", labelsize=13)
axes[1, 2].spines[["top", "right"]].set_visible(False)

plt.tight_layout(pad=3.0)
plt.savefig("fig3_demographics.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig3_demographics.png")

# FIG 6 · EDUCATION & ENGLISH PROFICIENCY

fig6, axes = plt.subplots(1, 2, figsize=(22, 10))
fig6.suptitle("Fig 6 · Education & English Proficiency (n=30)",
              fontsize=22, fontweight="bold")

# Get exact values directly from data
edu_counts = df["education"].value_counts()
eng_counts = df["english_proficiency"].value_counts()

print("Education exact values:")
print(edu_counts)
print("\nEnglish proficiency exact values:")
print(eng_counts)

# Reorder education from lowest to highest
edu_order4 = ["Middle School", "High School",
              [x for x in edu_counts.index if "achelor" in str(x)][0],
              "Graduate degree"]
edu_counts = edu_counts.reindex(
    [e for e in edu_order4 if e in edu_counts.index]
).fillna(0).astype(int)

# Reorder english proficiency
eng_order4 = ["Basic", "Intermediate", "Advanced"]
eng_counts = eng_counts.reindex(
    [e for e in eng_order4 if e in eng_counts.index]
).fillna(0).astype(int)

# Left chart — Education
colors_edu = sns.color_palette("tab10", len(edu_counts))
bars = axes[0].barh(range(len(edu_counts)), edu_counts.values,
                    color=colors_edu, edgecolor="white", linewidth=0.8)
for i, (bar, val) in enumerate(zip(bars, edu_counts.values)):
    axes[0].text(bar.get_width() + 0.1,
                 bar.get_y() + bar.get_height() / 2,
                 f"{val} ({val/30*100:.0f}%)",
                 va="center", fontsize=13, fontweight="bold")

# Use clean display labels
axes[0].set_yticks(range(len(edu_counts)))
axes[0].set_yticklabels(
    ["Middle School", "High School", "Bachelor's", "Graduate degree"],
    fontsize=13
)
axes[0].set_xlim(0, edu_counts.max() + 5)
axes[0].set_title("Educational Level", fontsize=18, fontweight="bold")
axes[0].set_xlabel("Count", fontsize=14)
axes[0].set_ylabel("", fontsize=14)
axes[0].tick_params(axis="x", labelsize=13)
axes[0].spines[["top", "right"]].set_visible(False)

# Right chart — English Proficiency
colors_eng = sns.color_palette("mako_r", len(eng_counts))
bars = axes[1].barh(range(len(eng_counts)), eng_counts.values,
                    color=colors_eng, edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, eng_counts.values):
    axes[1].text(bar.get_width() + 0.1,
                 bar.get_y() + bar.get_height() / 2,
                 f"{val} ({val/30*100:.0f}%)",
                 va="center", fontsize=13, fontweight="bold")

axes[1].set_yticks(range(len(eng_counts)))
axes[1].set_yticklabels(eng_order4, fontsize=13)
axes[1].set_xlim(0, eng_counts.max() + 5)
axes[1].set_title("English Proficiency", fontsize=18, fontweight="bold")
axes[1].set_xlabel("Count", fontsize=14)
axes[1].set_ylabel("", fontsize=14)
axes[1].tick_params(axis="x", labelsize=13)
axes[1].spines[["top", "right"]].set_visible(False)

plt.tight_layout(pad=3.0)
plt.savefig("fig6_education_language.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig6_education_language.png")

# FIG 7 · HEATMAP EDUCATION x ENGLISH PROFICIENCY

fig7, ax7 = plt.subplots(figsize=(12, 7))

# Build crosstab directly from raw columns
ct = pd.crosstab(df["education"], df["english_proficiency"])

# Reorder columns
eng_order5 = ["Basic", "Intermediate", "Advanced"]
ct = ct[[c for c in eng_order5 if c in ct.columns]]

# Reorder rows using exact values from data
edu_vals = df["education"].unique()
bachelors7 = [x for x in edu_vals if "achelor" in str(x)][0]
edu_order7 = ["Middle School", "High School", bachelors7, "Graduate degree"]
ct = ct.reindex([e for e in edu_order7 if e in ct.index])

# Rename index for clean display
ct.index = ["Middle School", "High School", "Bachelor's", "Graduate degree"]

print("Heatmap crosstab:")
print(ct)
print(f"Total: {ct.values.sum()}")

sns.heatmap(ct, annot=True, fmt="d", cmap="YlOrRd",
            linewidths=0.8, ax=ax7,
            annot_kws={"size": 16, "weight": "bold"},
            cbar_kws={"label": "Count", "shrink": 0.8})

ax7.set(title="Fig 7 · Education × English Proficiency (n=30)",
        xlabel="English Proficiency",
        ylabel="Education Level")
ax7.title.set_fontsize(16)
ax7.title.set_fontweight("bold")
ax7.xaxis.label.set_fontsize(14)
ax7.yaxis.label.set_fontsize(14)
ax7.tick_params(axis="both", labelsize=13)

plt.tight_layout()
plt.savefig("fig7_heatmap_edu_english.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig7_heatmap_edu_english.png")

# FIG 8 · ARRIVAL TIME IN SYRACUSE

fig8_arr, ax8_arr = plt.subplots(figsize=(16, 8))

arrival_map = {
    "Three years":        "3 years",
    "Four years":         "4 years",
    "Less than one year": "< 1 year",
    "One year":           "1 year",
    "17 years":           "17 years",
    "Two years":          "2 years",
    "20":                 "20 years",
    "2004":               "20+ years",
    "18":                 "18 years",
    "12 years":           "12 years",
    "9":                  "9 years",
    "7":                  "7 years",
    "15":                 "15 years",
    "Visiting":           "Exclude"
}

df6_arr = df.copy()
df6_arr["arrival_clean"] = df6_arr["arrival_year"].map(arrival_map)
df6_arr = df6_arr[
    df6_arr["arrival_clean"].notna() &
    (df6_arr["arrival_clean"] != "Exclude")
]

arr_order = ["< 1 year", "1 year", "2 years", "3 years", "4 years",
             "7 years", "9 years", "12 years", "15 years",
             "17 years", "18 years", "20 years", "20+ years"]

arr_counts = df6_arr["arrival_clean"].value_counts().reindex(
    arr_order).fillna(0).astype(int)

total_arr = arr_counts.sum()
print(f"Total: {total_arr}")

colors_a = sns.color_palette("Blues_d", len(arr_counts))
bars = ax8_arr.bar(arr_counts.index, arr_counts.values,
                   color=colors_a, edgecolor="white", linewidth=0.8)

# Add count AND percentage labels
for bar, val in zip(bars, arr_counts.values):
    if val > 0:
        pct = val / total_arr * 100
        ax8_arr.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.1,
            f"{val}\n({pct:.0f}%)",
            ha="center", fontsize=10, fontweight="bold"
        )

ax8_arr.set(title="Fig 8 · How Long Ago Participants Arrived in Syracuse",
            xlabel="Years Since Arrival",
            ylabel="Number of Respondents")
ax8_arr.title.set_fontsize(16)
ax8_arr.title.set_fontweight("bold")
ax8_arr.xaxis.label.set_fontsize(14)
ax8_arr.yaxis.label.set_fontsize(14)
ax8_arr.set_xticklabels(arr_counts.index, rotation=30,
                        ha="right", fontsize=12)
ax8_arr.set_ylim(0, arr_counts.max() + 2)
ax8_arr.yaxis.grid(True, linestyle="--", alpha=0.5, color="gray")
ax8_arr.set_axisbelow(True)
sns.despine(ax=ax8_arr)

plt.tight_layout()
plt.savefig("fig8_arrival_time.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig8_arrival_time.png")

# FIG 9 · EMPLOYMENT

fig9, axes = plt.subplots(1, 2, figsize=(22, 10))
fig9.suptitle("Fig 9 · Employment (n=30)",
              fontsize=22, fontweight="bold")

# Profession
prof_counts = df["profession"].value_counts()
colors_p = sns.color_palette("tab10", len(prof_counts))
bars = axes[0].barh(prof_counts.index, prof_counts.values,
                     color=colors_p, edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, prof_counts.values):
    axes[0].text(bar.get_width() + 0.1,
                 bar.get_y() + bar.get_height() / 2,
                 f"{val} ({val/30*100:.0f}%)",
                 va="center", fontsize=13, fontweight="bold")
axes[0].set_xlim(0, prof_counts.max() + 4)
axes[0].set_title("Profession", fontsize=18, fontweight="bold")
axes[0].set_xlabel("Count", fontsize=14)
axes[0].set_ylabel("", fontsize=14)
axes[0].tick_params(axis="both", labelsize=13)
axes[0].spines[["top", "right"]].set_visible(False)

# Time to find job — map from text directly
job_text_map = {
    "Less than 3 months": "< 3 months",
    "Six months":         "6 months",
    "One year":           "1 year",
    "Two years":          "2 years",
    "Three years":        "3 years"
}
df["job_label"] = df["time_to_find_job"].map(job_text_map)
job_order = ["< 3 months", "6 months", "1 year", "2 years", "3 years"]
job_counts = df["job_label"].value_counts().reindex(job_order).fillna(0).astype(int)

colors_j = sns.color_palette("mako_r", len(job_order))
bars = axes[1].barh(job_order, job_counts.values,
                     color=colors_j, edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, job_counts.values):
    if val > 0:
        axes[1].text(bar.get_width() + 0.1,
                     bar.get_y() + bar.get_height() / 2,
                     f"{val} ({val/26*100:.0f}%)",
                     va="center", fontsize=13, fontweight="bold")
axes[1].set_xlim(0, job_counts.max() + 4)
axes[1].set_title("Time to Find a Job After Arriving (n=26)",
                  fontsize=18, fontweight="bold")
axes[1].set_xlabel("Count", fontsize=14)
axes[1].set_ylabel("", fontsize=14)
axes[1].tick_params(axis="both", labelsize=13)
axes[1].spines[["top", "right"]].set_visible(False)

plt.tight_layout(pad=3.0)
plt.savefig("fig9_employment.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig9_employment.png")

# FIG 10 · TIME TO FIND JOB BAR CHART

fig10, ax10 = plt.subplots(figsize=(14, 8))

job_counts10 = df["job_label"].value_counts().reindex(job_order).fillna(0).astype(int)
colors_t = sns.color_palette("YlOrRd", len(job_order))
bars = ax10.bar(job_order, job_counts10.values,
               color=colors_t, edgecolor="white", linewidth=0.8)

for bar, val in zip(bars, job_counts10.values):
    if val > 0:
        pct = val / 26 * 100
        ax10.text(bar.get_x() + bar.get_width() / 2,
                 val + 0.1, f"{val}\n({pct:.0f}%)",
                 ha="center", fontsize=13, fontweight="bold")

ax10.set(title="Fig 10 · Time to Find a Job After Arriving in Syracuse (n=26)",
        xlabel="Time to Find a Job",
        ylabel="Number of Respondents")
ax10.set_ylim(0, job_counts10.max() + 3)
ax10.title.set_fontsize(16)
ax10.title.set_fontweight("bold")
ax10.xaxis.label.set_fontsize(14)
ax10.yaxis.label.set_fontsize(14)
ax10.tick_params(axis="both", labelsize=13)
sns.despine(ax=ax10)

plt.tight_layout()
plt.savefig("fig10_time_to_find_job.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig10_time_to_find_job.png")


# FIG 11 · ENGLISH PROFICIENCY VS TIME TO FIND A JOB

fig11_eng, ax11_eng = plt.subplots(figsize=(14, 9))

# Map text to numbers
eng_num_map = {"Basic": 1, "Intermediate": 2, "Advanced": 3}
job_text_map = {
    "Less than 3 months": 1,
    "Six months":         2,
    "One year":           3,
    "Two years":          4,
    "Three years":        5
}

df11 = df.copy()
df11["eng_num"] = df11["english_proficiency"].map(eng_num_map)
df11["job_num"] = df11["time_to_find_job"].map(job_text_map)
df11 = df11[df11["eng_num"].notna() & df11["job_num"].notna()]

print(f"Total rows for Fig 11: {len(df11)}")
print("English proficiency counts:")
print(df11["english_proficiency"].value_counts())
print("Time to find job counts:")
print(df11["time_to_find_job"].value_counts())

# Count exact combinations for labels
combo_counts = df11.groupby(
    ["eng_num", "job_num", "english_proficiency"]
).size().reset_index(name="count")
print("\nCombination counts:")
print(combo_counts)

# Add jitter
np.random.seed(42)
df11["eng_j"] = df11["eng_num"] + np.random.uniform(-0.08, 0.08, len(df11))
df11["job_j"] = df11["job_num"] + np.random.uniform(-0.08, 0.08, len(df11))

# Plot colored dots by proficiency level
colors_s = {
    "Basic":        "#e74c3c",
    "Intermediate": "#f39c12",
    "Advanced":     "#2ecc71"
}
for level, group in df11.groupby("english_proficiency"):
    ax11_eng.scatter(
        group["eng_j"], group["job_j"],
        label=level,
        color=colors_s[level],
        s=200,
        edgecolor="white",
        linewidth=1.2,
        alpha=0.9,
        zorder=5
    )

# Add count labels for combinations with more than 1
for _, row in combo_counts.iterrows():
    if row["count"] > 1:
        ax11_eng.annotate(
            f"n={int(row['count'])}",
            xy=(row["eng_num"], row["job_num"]),
            xytext=(12, 5),
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
            color="#2c3e50",
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="white",
                edgecolor="gray",
                alpha=0.8
            )
        )

# Trend line
xv = df11["eng_num"].values
yv = df11["job_num"].values
m, b = np.polyfit(xv, yv, 1)
xs  = np.linspace(0.8, 3.2, 100)
ax11_eng.plot(xs, m * xs + b, color="#E76F51",
             lw=2.5, ls="--", label="Trend", zorder=3)

# Axis settings
ax11_eng.set_xticks([1, 2, 3])
ax11_eng.set_xticklabels(["Basic", "Intermediate", "Advanced"], fontsize=13)
ax11_eng.set_yticks([1, 2, 3, 4, 5])
ax11_eng.set_yticklabels(["< 3 months", "6 months", "1 year",
                          "2 years", "3 years"], fontsize=13)
ax11_eng.set_xlim(0.5, 3.5)
ax11_eng.set_ylim(0.5, 5.8)

# Grid lines
ax11_eng.yaxis.grid(True, linestyle="--", alpha=0.5, color="gray")
ax11_eng.xaxis.grid(True, linestyle="--", alpha=0.3, color="gray")
ax11_eng.set_axisbelow(True)

ax11_eng.set_title("Fig 11 · English Proficiency vs Time to Find a Job (n=26)",
                  fontsize=16, fontweight="bold")
ax11_eng.set_xlabel("English Proficiency Level", fontsize=14)
ax11_eng.set_ylabel("Time to Find a Job", fontsize=14)
ax11_eng.legend(fontsize=12, title="Proficiency",
               title_fontsize=13, loc="upper left")
sns.despine(ax=ax11_eng)

plt.tight_layout()
plt.savefig("fig11_english_job.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig11_english_job.png")


# Figure 12
# EXACT MAPPINGS FROM YOUR DATA
inc_label_map = {
    "$500 to $1000":         "$500-1k",
    "$3000 or more":         "$3k+",
    "$1000 to $2000":        "$1k-2k",
    "$100 to $500":          "$100-500",
    "Weekly $500 to $1000":  "$500-1k"
}
pct_label_map = {
    "76 - 100%":   "76-100%",
    "51 - 75%":    "51-75%",
    "26 - 50%":    "26-50%",
    "25% or less": "≤ 25%"
}
inc_num_map = {
    "$500 to $1000":         750,
    "$3000 or more":        3000,
    "$1000 to $2000":       1500,
    "$100 to $500":          300,
    "Weekly $500 to $1000":  750
}
pct_num_map = {
    "76 - 100%":   4,
    "51 - 75%":    3,
    "26 - 50%":    2,
    "25% or less": 1
}

df["inc_label"] = df["income"].map(inc_label_map)
df["pct_label"] = df["pct_income_local"].map(pct_label_map)

# FIG 12 · INCOME

fig12, axes = plt.subplots(1, 3, figsize=(24, 8))
fig12.suptitle("Fig 12 · Income Distribution (n=29)",
              fontsize=22, fontweight="bold")

# Income frequency
freq_counts = df["income_frequency"].value_counts()
bars = axes[0].barh(freq_counts.index, freq_counts.values,
                    color=sns.color_palette("Set2", len(freq_counts)),
                    edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, freq_counts.values):
    axes[0].text(bar.get_width() + 0.1,
                 bar.get_y() + bar.get_height() / 2,
                 f"{val} ({val/30*100:.0f}%)",
                 va="center", fontsize=13, fontweight="bold")
axes[0].set_xlim(0, freq_counts.max() + 5)
axes[0].set_title("Income Payment Frequency", fontsize=16, fontweight="bold")
axes[0].set_xlabel("Count", fontsize=14)
axes[0].set_ylabel("", fontsize=14)
axes[0].tick_params(axis="both", labelsize=13)
axes[0].spines[["top", "right"]].set_visible(False)

# Income level
inc_order = ["$100-500", "$500-1k", "$1k-2k", "$3k+"]
inc_counts = df["inc_label"].value_counts().reindex(inc_order).fillna(0).astype(int)
bars = axes[1].barh(inc_order, inc_counts.values,
                    color=sns.color_palette("Blues", len(inc_order)),
                    edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, inc_counts.values):
    axes[1].text(bar.get_width() + 0.1,
                 bar.get_y() + bar.get_height() / 2,
                 f"{val} ({val/29*100:.0f}%)" if val > 0 else "0",
                 va="center", fontsize=13, fontweight="bold")
axes[1].set_xlim(0, inc_counts.max() + 4)
axes[1].set_title("Income Level (n=29)", fontsize=16, fontweight="bold")
axes[1].set_xlabel("Count", fontsize=14)
axes[1].set_ylabel("", fontsize=14)
axes[1].tick_params(axis="both", labelsize=13)
axes[1].spines[["top", "right"]].set_visible(False)

# % Income spent locally
pct_order = ["≤ 25%", "26-50%", "51-75%", "76-100%"]
pct_counts = df["pct_label"].value_counts().reindex(pct_order).fillna(0).astype(int)
bars = axes[2].barh(pct_order, pct_counts.values,
                    color=sns.color_palette("YlOrBr", len(pct_order)),
                    edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, pct_counts.values):
    axes[2].text(bar.get_width() + 0.1,
                 bar.get_y() + bar.get_height() / 2,
                 f"{val} ({val/29*100:.0f}%)" if val > 0 else "0",
                 va="center", fontsize=13, fontweight="bold")
axes[2].set_xlim(0, pct_counts.max() + 4)
axes[2].set_title("% Income Spent Locally (n=29)",
                  fontsize=16, fontweight="bold")
axes[2].set_xlabel("Count", fontsize=14)
axes[2].set_ylabel("", fontsize=14)
axes[2].tick_params(axis="both", labelsize=13)
axes[2].spines[["top", "right"]].set_visible(False)

plt.tight_layout(pad=3.0)
plt.savefig("fig12_income.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig12_income.png")

# FIG 13 · EDUCATION VS INCOME

fig13, ax11 = plt.subplots(figsize=(14, 8))

# Get exact Bachelor's value from data
bachelors = [x for x in df["education"].unique() if "achelor" in str(x)][0]
print(f"Exact Bachelor's value: {repr(bachelors)}")

# Income mapping
inc_label_map10 = {
    "$500 to $1000":         "$500-1k",
    "$3000 or more":         "$3k+",
    "$1000 to $2000":        "$1k-2k",
    "$100 to $500":          "$100-500",
    "Weekly $500 to $1000":  "$500-1k"
}

df11 = df.copy()

# Use education directly — no fillna needed
df11["edu_label"] = df11["education"]
df11["inc_label"] = df11["income"].map(inc_label_map10)

# Fix missing income — assign to $500-1k
mask11 = df11["inc_label"].isna() & df11["edu_label"].notna()
df11.loc[mask11, "inc_label"] = "$500-1k"

# Keep only valid rows
df11 = df11[df11["inc_label"].notna() & df11["edu_label"].notna()]

print(f"Total rows: {len(df11)}")
print("Education counts:")
print(df11["edu_label"].value_counts())

# Build crosstab
ct11 = pd.crosstab(df11["edu_label"], df11["inc_label"])

# Reorder using exact values from data
edu_order11 = ["Middle School", "High School", bachelors, "Graduate degree"]
inc_order11  = ["$100-500", "$500-1k", "$1k-2k", "$3k+"]
ct10 = ct11.reindex([e for e in edu_order11 if e in ct11.index])
ct10 = ct11[[c for c in inc_order11 if c in ct11.columns]]

print("\nEducation vs Income crosstab:")
print(ct11)
print(f"\nTotal: {ct11.values.sum()}")

# Rename index for display
ct11.index = ["Middle School", "High School", "Bachelor's", "Graduate degree"]

ct11.plot(kind="bar", ax=ax11, colormap="RdYlGn",
          edgecolor="white", linewidth=0.6, width=0.75)
for container in ax11.containers:
    ax11.bar_label(container, fmt="%d", fontsize=11, padding=3)

ax11.set_title("Fig 13 · Education Level vs Income",
               fontsize=16, fontweight="bold")
ax11.set_xlabel("Education Level", fontsize=14)
ax11.set_ylabel("Number of Respondents", fontsize=14)
ax11.set_xticklabels(ax11.get_xticklabels(), rotation=0, fontsize=13)
ax11.legend(title="Income Range", fontsize=12, title_fontsize=13)
ax11.set_ylim(0, ct10.values.max() + 2)
sns.despine(ax=ax11)

plt.tight_layout()
plt.savefig("fig13_education_income.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig13_education_income.png")

# FIG 14 · INCOME VS % SPENT LOCALLY

fig14, ax14 = plt.subplots(figsize=(12, 8))

inc_num_map = {
    "$500 to $1000":         750,
    "$3000 or more":        3000,
    "$1000 to $2000":       1500,
    "$100 to $500":          300,
    "Weekly $500 to $1000":  750
}
pct_num_map = {
    "76 - 100%":   4,
    "51 - 75%":    3,
    "26 - 50%":    2,
    "25% or less": 1
}

df12 = df.copy()
df12["inc_num"] = df12["income"].map(inc_num_map)
df12["pct_num"] = df12["pct_income_local"].map(pct_num_map)
df12 = df12[df12["inc_num"].notna() & df12["pct_num"].notna()]

# Count exact combinations
combo = df12.groupby(["inc_num", "pct_num"]).size().reset_index(name="count")
print("Exact counts per combination:")
print(combo)

# Add jitter
np.random.seed(42)
df12["inc_j"] = df12["inc_num"] + np.random.uniform(-20, 20, len(df12))
df12["pct_j"] = df12["pct_num"] + np.random.uniform(-0.08, 0.08, len(df12))

sc12 = ax14.scatter(df12["inc_j"], df12["pct_j"],
                    c=df12["inc_num"], cmap="Blues",
                    edgecolors="#2c3e50", linewidths=0.8,
                    s=150, alpha=0.9, zorder=3)

# Add count labels on each combination
for _, row in combo.iterrows():
    ax14.annotate(
        f"n={int(row['count'])}",
        xy=(row["inc_num"], row["pct_num"]),
        xytext=(15, 8),
        textcoords="offset points",
        fontsize=11,
        fontweight="bold",
        color="#2c3e50",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="white",
            edgecolor="#2c3e50",
            alpha=0.9,
            linewidth=1.2
        ),
        arrowprops=dict(
            arrowstyle="->",
            color="#2c3e50",
            linewidth=1.0
        )
    )

# Trend line
xv = df12["inc_num"].values
yv = df12["pct_num"].values
m, b = np.polyfit(xv, yv, 1)
xs  = np.linspace(200, 3200, 100)
ax14.plot(xs, m * xs + b, color="#E76F51",
          lw=2.5, ls="--", label="Trend")

# Axis settings
ax14.set_xticks([300, 750, 1500, 3000])
ax14.set_xticklabels(["$100-500", "$500-1k", "$1k-2k", "$3k+"],
                      fontsize=13)
ax14.set_yticks([1, 2, 3, 4])
ax14.set_yticklabels(["≤ 25%", "26-50%", "51-75%", "76-100%"],
                      fontsize=13)
ax14.set_xlim(100, 3400)
ax14.set_ylim(0.5, 4.8)

# Grid
ax14.yaxis.grid(True, linestyle="--", alpha=0.5, color="gray")
ax14.xaxis.grid(True, linestyle="--", alpha=0.3, color="gray")
ax14.set_axisbelow(True)

ax14.set_title("Fig 14 · Income vs % of Income Spent Locally (n=29)",
               fontsize=16, fontweight="bold")
ax14.set_xlabel("Income Level", fontsize=14)
ax14.set_ylabel("% Income Spent Locally", fontsize=14)
ax14.legend(fontsize=12)

cbar = fig14.colorbar(sc12, ax=ax14, fraction=0.03, pad=0.02)
cbar.set_label("Income (mid-point $)", fontsize=12)
cbar.ax.tick_params(labelsize=11)
sns.despine(ax=ax14)

plt.tight_layout()
plt.savefig("fig14_income_local.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig14_income_local.png")

# FIG 15 · COMMUNITY VOLUNTEERING

fig15, axes = plt.subplots(1, 2, figsize=(22, 10))
fig15.suptitle("Fig 15 · Community Volunteering (n=30)",
               fontsize=22, fontweight="bold")

# Yes/No chart
vol_counts = df["volunteers"].value_counts()
colors_v   = ["#2ecc71" if x == "Yes" else "#e74c3c"
               for x in vol_counts.index]
bars = axes[0].bar(vol_counts.index, vol_counts.values,
                    color=colors_v, edgecolor="white", linewidth=0.8)
for bar, val in zip(bars, vol_counts.values):
    axes[0].text(bar.get_x() + bar.get_width() / 2,
                 val + 0.2, f"{val}\n({val/30*100:.0f}%)",
                 ha="center", fontsize=13, fontweight="bold")
axes[0].set(title="Volunteers in the Community?",
            xlabel="", ylabel="Count")
axes[0].set_ylim(0, vol_counts.max() + 4)
axes[0].title.set_fontsize(18)
axes[0].title.set_fontweight("bold")
axes[0].tick_params(axis="both", labelsize=13)
axes[0].yaxis.label.set_fontsize(14)
axes[0].spines[["top", "right"]].set_visible(False)

# Word frequency
stopwords = {"i", "to", "in", "the", "and", "a", "of", "for",
             "my", "is", "when", "they", "are", "it", "with",
             "have", "at", "or", "our", "that", "we"}
words = (df["volunteer_details"].dropna()
         .str.lower()
         .str.replace(r"[^a-z\s]", " ", regex=True)
         .str.split().explode())
words = words[~words.isin(stopwords) & (words.str.len() > 2)]
top_words = words.value_counts().head(15)

colors_w = sns.color_palette("husl", len(top_words))
bars = axes[1].barh(top_words.index, top_words.values,
                     color=colors_w, edgecolor="white", linewidth=0.6)
for bar, val in zip(bars, top_words.values):
    axes[1].text(bar.get_width() + 0.03,
                 bar.get_y() + bar.get_height() / 2,
                 str(val), va="center", fontsize=12)
axes[1].set_xlim(0, top_words.max() * 1.35)
axes[1].set(title="Top Words in Volunteer Descriptions",
            xlabel="Frequency", ylabel="")
axes[1].title.set_fontsize(18)
axes[1].title.set_fontweight("bold")
axes[1].tick_params(axis="both", labelsize=13)
axes[1].xaxis.label.set_fontsize(14)
axes[1].spines[["top", "right"]].set_visible(False)

plt.tight_layout(pad=3.0)
plt.savefig("fig15_volunteering.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig15_volunteering.png")


