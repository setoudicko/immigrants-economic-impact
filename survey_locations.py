#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:29:55 2026

@author: agaichatoudicko
"""

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx
import zipfile
import os

# 1. Interview locations
locations = pd.DataFrame({
    "place": [
        "North Salina Street",
        "Destiny USA Mall",
        "Syracuse University Avenue",
        "Walmart",
        "Online (Syracuse)"
    ],
    "lat": [
        43.0631,
        43.0712,
        43.0385,
        43.0451,
        43.0481
    ],
    "lon": [
        -76.1474,
        -76.1692,
        -76.1331,
        -76.1821,
        -76.1474
    ],
    "color": [
        "#e74c3c",
        "#3498db",
        "#2ecc71",
        "#f39c12",
        "#9b59b6"
    ]
})

# 2. Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    locations,
    geometry=[Point(lon, lat) for lon, lat in
              zip(locations["lon"], locations["lat"])],
    crs="EPSG:4326"
)

# Convert to Web Mercator for basemap
gdf = gdf.to_crs(epsg=3857)

# 3. FIG 1 · Syracuse Locations Map
fig1, ax17 = plt.subplots(1, 1, figsize=(16, 14))

# Plot each location
for _, row in gdf.iterrows():
    ax17.scatter(
        row.geometry.x,
        row.geometry.y,
        s=400,
        color=row["color"],
        edgecolor="white",
        linewidth=2.0,
        zorder=5,
        alpha=0.9
    )

# Add labels with offsets for each location
label_offsets = {
    "North Salina Street":        ( 15,   15),
    "Destiny USA Mall":           ( 15,   15),
    "Syracuse University Avenue": ( 15,  -25),
    "Walmart":                    (-15,   15),
    "Online (Syracuse)":          ( 15,  -25)
}

for _, row in gdf.iterrows():
    offset = label_offsets.get(row["place"], (15, 15))
    ax17.annotate(
        row["place"],
        xy=(row.geometry.x, row.geometry.y),
        xytext=offset,
        textcoords="offset points",
        fontsize=13,
        fontweight="bold",
        color="#2c3e50",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="white",
            edgecolor=row["color"],
            alpha=0.95,
            linewidth=2.0
        ),
        arrowprops=dict(
            arrowstyle="->",
            color=row["color"],
            linewidth=1.5
        )
    )

# Add basemap
try:
    ctx.add_basemap(
        ax17,
        source=ctx.providers.OpenStreetMap.Mapnik,
        zoom=14
    )
    print("Basemap loaded successfully")
except Exception as e:
    print(f"Basemap not loaded: {e}")
    ax17.set_facecolor("#f0f0f0")

# Title
ax17.set_title(
    "Fig 1 · Survey Data Collection Locations in Syracuse, NY\n"
    "The Economic Impact of Foreign-Born Residents (n=30)",
    fontsize=16,
    fontweight="bold",
    pad=20
)
ax17.set_axis_off()

# Legend
legend_elements = [
    plt.scatter([], [], s=200,
                color=row["color"],
                edgecolor="white",
                label=row["place"])
    for _, row in locations.iterrows()
]
ax17.legend(
    handles=legend_elements,
    fontsize=12,
    loc="lower right",
    framealpha=0.95,
    edgecolor="gray",
    title="Interview Locations",
    title_fontsize=13
)

# Add note
ax17.text(
    0.01, 0.01,
    "Note: Interviews conducted at physical locations\n"
    "and online during March - April 2026",
    transform=ax17.transAxes,
    fontsize=11,
    color="gray",
    style="italic",
    bbox=dict(
        boxstyle="round,pad=0.4",
        facecolor="white",
        edgecolor="gray",
        alpha=0.8
    )
)

plt.tight_layout()
plt.savefig("fig1_survey_locations.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("Saved fig1_survey_locations.png")