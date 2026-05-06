#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 19:35:41 2026

@author: agaichatoudicko
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import zipfile
import os

# 1. Load data
df = pd.read_csv("Survey for foreign-born residents of Syracuse _2026-04-04.csv")
df = df.rename(columns={"What is your country of origin?": "country_of_origin"})

# Strip extra spaces from country names
df["country_of_origin"] = df["country_of_origin"].str.strip()

# 2. Clean country names
country_clean = {
    "Somalia":            "Somalia",
    "Nigeria":            "Nigeria",
    "Turkey":             "Turkey",
    "Burundi":            "Burundi",
    "Afghanistan":        "Afghanistan",
    "Tanzania":           "Tanzania",
    "Cuba":               "Cuba",
    "Korea, Republic of": "South Korea",
    "Indonesia":          "Indonesia",
    "India":              "India",
    "Syria":              "Syria",
    "Pakistan":           "Pakistan",
    "Haïti":              "Haiti",
    "Bangladesh":         "Bangladesh",
    "Ghana":              "Ghana",
    "Yemen":              "Yemen",
    "YEMEN":              "Yemen",
    "Iraq":               "Iraq"
}

df["country_clean"] = df["country_of_origin"].map(country_clean)

# 3. Count respondents per country
country_counts = df["country_clean"].value_counts().reset_index()
country_counts.columns = ["country", "count"]
print("Respondents per country:")
print(country_counts)
print(f"Total countries: {len(country_counts)}")

#  4. Unzip shapefile
zip_path = "ne_10m_admin_0_countries.zip"
extract_path = "ne_10m_admin_0_countries"

if not os.path.exists(extract_path):
    print("Extracting shapefile...")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_path)
    print("Extracted successfully")

# Load shapefile
world = gpd.read_file(os.path.join(extract_path, "ne_10m_admin_0_countries.shp"))
print("\nShapefile loaded successfully")
print("Columns:", world.columns.tolist())

# 5. Find exact country names in shapefile
print("\nSearching for country name matches:")
countries_to_find = [
    "Somalia", "Nigeria", "Turkey", "Burundi", "Afghanistan",
    "Tanzania", "Cuba", "Korea", "Indonesia", "India",
    "Syria", "Pakistan", "Haiti", "Bangladesh", "Ghana",
    "Yemen", "Iraq"
]
for country in countries_to_find:
    match = world[world["NAME"].str.contains(
        country, case=False, na=False)]["NAME"].tolist()
    print(f"{country:15} → {match}")

# 6. Rename name column
world = world.rename(columns={"NAME": "name"})

# 7. Fix country name mismatches
# These map your cleaned names to exact shapefile names
name_fix = {
    "Somalia":     "Somalia",
    "Nigeria":     "Nigeria",
    "Turkey":      "Turkey",
    "Burundi":     "Burundi",
    "Afghanistan": "Afghanistan",
    "Tanzania":    "Tanzania",
    "Cuba":        "Cuba",
    "South Korea": "South Korea",
    "Indonesia":   "Indonesia",
    "India":       "India",
    "Syria":       "Syria",
    "Pakistan":    "Pakistan",
    "Haiti":       "Haiti",
    "Bangladesh":  "Bangladesh",
    "Ghana":       "Ghana",
    "Yemen":       "Yemen",
    "Iraq":        "Iraq"
}

country_counts["name"] = country_counts["country"].map(name_fix)

# 8. Merge data with shapefile
world = world.merge(country_counts, on="name", how="left")
print("\nMatched countries:")
print(world[world["count"].notna()][["name", "count"]])
print(f"Total matched: {world['count'].notna().sum()}")

# Fix manual label offsets
label_offsets = {
    # Cuba and Haiti — spread vertically
    "Cuba":        (-120,  50),   # move Cuba higher up
    "Haiti":       (-120, -30),   # move Haiti lower down

    # Syria and Iraq — spread apart
    "Syria":       (-100,  70),   # move Syria higher up
    "Iraq":        (-100, -50),   # move Iraq lower down

    # Afghanistan and South Korea — spread apart
    "Afghanistan": ( 80,   100),   # move Afghanistan higher
    "South Korea": ( 120,  -80),   # move South Korea lower

    # Others — keep spread out
    "Somalia":     ( 80,  -70),
    "Nigeria":     (-80,  -60),
    "Turkey":      ( 40,   60),
    "Burundi":     (-100,  20),
    "Tanzania":    ( 70,  -80),
    "Indonesia":   ( 70,  -40),
    "India":       ( 80,  -50),
    "Pakistan":    ( 80,   60),
    "Bangladesh":  ( 100, -50),
    "Ghana":       (-100, -50),
    "Yemen":       ( 80,  -60)
}

# 10. FIG 4 · World Map
fig4, ax4 = plt.subplots(1, 1, figsize=(28, 16))

# Base map — all countries light gray
world[world["count"].isna()].plot(
    ax=ax4,
    color="#d3d3d3",
    edgecolor="white",
    linewidth=0.5
)

# Highlighted countries
world[world["count"].notna()].plot(
    ax=ax4,
    column="count",
    cmap="YlOrRd",
    edgecolor="white",
    linewidth=0.8,
    legend=True,
    legend_kwds={
        "label":       "Number of Respondents",
        "orientation": "horizontal",
        "shrink":      0.4,
        "pad":         0.02,
        "aspect":      30
    }
)

# Add labels with manual offsets
for _, row in world[world["count"].notna()].iterrows():
    centroid = row.geometry.centroid
    offset = label_offsets.get(row["name"], (15, 15))
    ax4.annotate(
        text=f"{row['name']}\n(n={int(row['count'])})",
        xy=(centroid.x, centroid.y),
        xytext=offset,
        textcoords="offset points",
        fontsize=11,
        fontweight="bold",
        color="#2c3e50",
        bbox=dict(
            boxstyle="round,pad=0.4",
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

# Syracuse marker
ax4.plot(-76.1474, 43.0481,
         marker="*",
         color="#e74c3c",
         markersize=22,
         zorder=5)
ax4.annotate(
    "Syracuse, NY\n(Destination)",
    xy=(-76.1474, 43.0481),
    xytext=(-80, 20),
    textcoords="offset points",
    fontsize=12,
    fontweight="bold",
    color="#e74c3c",
    bbox=dict(
        boxstyle="round,pad=0.4",
        facecolor="white",
        edgecolor="#e74c3c",
        alpha=0.9,
        linewidth=1.5
    ),
    arrowprops=dict(
        arrowstyle="->",
        color="#e74c3c",
        linewidth=1.2
    )
)

ax4.set_title(
    "Fig 4 · Countries of Origin of Foreign-Born Residents "
    "in Syracuse, NY (n=30)",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax4.set_axis_off()

plt.tight_layout()
plt.savefig("fig4_world_map.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig4_world_map.png")

# 11. FIG 5 · Countries bar chart
fig5, ax5 = plt.subplots(figsize=(14, 10))

country_sorted = country_counts.sort_values("count", ascending=True)
colors = plt.cm.YlOrRd(
    np.linspace(0.3, 0.9, len(country_sorted))
)

bars = ax5.barh(
    country_sorted["country"],
    country_sorted["count"],
    color=colors,
    edgecolor="white",
    linewidth=0.8
)

total = country_counts["count"].sum()
for bar, val in zip(bars, country_sorted["count"]):
    pct = val / total * 100
    ax5.text(
        bar.get_width() + 0.05,
        bar.get_y() + bar.get_height() / 2,
        f"{val} ({pct:.1f}%)",
        va="center",
        fontsize=12,
        fontweight="bold"
    )

ax5.set_xlim(0, country_sorted["count"].max() + 2)
ax5.set(
    title="Fig 5 · Country of Origin of Survey Respondents (n=30)",
    xlabel="Number of Respondents",
    ylabel="Country"
)
ax5.title.set_fontsize(16)
ax5.title.set_fontweight("bold")
ax5.tick_params(axis="both", labelsize=13)
ax5.xaxis.label.set_fontsize(13)
ax5.yaxis.label.set_fontsize(13)
ax5.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
plt.savefig("fig5_country_bar.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig5_country_bar.png")


