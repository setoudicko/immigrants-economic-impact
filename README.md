# The Economic Impact of International Immigrants in Syracuse, NY

## Spring 2026

## By Agaichatou O. Dicko

## Overview

This research project employs six python scripts to process, analyze, and visualize primary survey data collected from 30 international immigrants in Syracuse. All scripts read from a single CSV data file and produce high resolution PNG figures. The scripts are designed to be run sequentially, beginning with data quality assessment and proceeding through descriptive analysis, geographic visualization, statistical summary, inter-variable analysis, and path modeling.

## Significance of the Study

This study used empirical data to assess the economic impact of immigrants in Syracuse. The primary survey data provides adding value through new complementary raw data and filling the gap in existing research that relies on census data.

# Input Data

This study used a survey research questionnaire designed and administered using Google Forms to collect quantitative and qualitative data on the economic contribution of international immigrants in Syracuse. The survey link was distributed through multiple digital channels including QR code, WhatsApp, and Instagram messages. Additionally, the researcher conducted in-person data collection with immigrants at North Salina Street, Destiny USA Mall, Syracuse University Avenue and Walmart.
Google Forms automatically stored all survey responses in both Excel and CSV formats. The CSV file was imported into Python for data cleaning, analysis and visualization.

## Questions asked to respondents

- What is your gender?
- Were you born in the U.S.?
- What is your marital status?
- Do you have children?
- If yes, how many children do you have?
- How old are you?
- What is your country of origin?
- What is your educational level?
- What is your English skill proficiency?
- When did you arrive in Syracuse?
- What is your profession?
- After arriving in Syracuse, how long does it take to find a job?
- What is the frequency of your income payment?
- How much do you earn as income?
- Approximately what percentage of your income is spent locally?
- Do you currently volunteer in any community service activities?
- If yes, please specify:

## Csv file containing variables information found on Google forms

"Survey for foreign-born residents of Syracuse _2026-04-04.csv"

Location: Same folder as all scripts
Rows: 30 respondents
Columns: 17 survey questions

This research sample and sampling techniques only focused on foreign-born residents of Syracuse who have a job and earn an income. Among the wide range of international immigrants from many nationalities, only 30 people responded to the questionnaire due to the current U.S. government immigration laws. Most of the participants were not willing to take part in the research survey.
Participation in the survey research was voluntary. Respondents’ identities were kept anonymous. 

## Required Libraries

 pandas
 numpy
 matplotlib
 seaborn
 scipy
 os
 geopandas
 contextily

## Scripts 

The following srcipts helped produce 18 figures related to the survey study.

1. [Survey_missing_data.py](survey_missing_data.py)

This script is the first to be run as it assesses the quality of the survey data before any analysis begins. It scans all columns of the CSV file for missing values, calculates the count and percentage of missing responses per variables, and generates a visual summary of data completeness. Running this script first ensures that the analysis is aware of any gaps in the data before proceeding with subsequent analyses.

2. [Survey_locations.py](Survey_locations.py)

This script generates a geographic map of Syracuse, New York showing the five locations where survey data were collected. It uses coordinate data to plot location markers on a city map, providing a visual representation of the spatial distribution of data collection sites. This figure appears in the methodology chapter to contextualize the survey sampling strategy.

3. [Survey_analysis.py](survey_analysis.py)

This generates eleven figures covering all major aspects of the survey findings including demographic profile, educational attainment versus English proficiency, arrival time, employment patterns, income distribution, and community volunteering. 

4. [Survey_maps.py](survey_maps.py)

This script generates geographic visualizations of the countries of origin of survey respondents. It combines survey data with Natural Earth world shapefiles to produce a choropleth world map and a companion bar chart. The script requires the geopandas library and the Natural Earth shapefile dataset to be downloaded separately.

5. [Survey_statistics.py](survey_statistics.py)

This script generates the descriptive statistical summary of the six key quantitative variables analyzed in the study. It converts all ordinal text variables to numeric scales using standardized mappings, calculates mean, median, and standard deviation for each variable, and produces histogram figures with statistical overlays.

6. [Path_analysis.py](path_analysis.py)

This script performs the advanced statistical analysis of the study by generating the correlation matrix and path diagram. It uses Pearson correlation coefficients to quantify the relationships between the four key economic variables — education, English proficiency, income, and percentage of income spent locally — and visualizes these relationships in three interconnected figures. This script requires the scipy library for statistical calculations.

## Visualization

Figure 1 presents a geographic map of Syracuse illustrating the locations where data were collected.

![text](images/fig1_survey_locations.png)

Figure 2 presents a horizontal bar chart summarizing the missing values across all variables.

![text](images/fig2_missing_data.png)

Figure 3 presents the demographic profile of survey respondents.

![text](images/fig3_demographics.png)

Figure 4 presents the geographic distribution of respondents' countries of origin on a choropleth world map.

![text](images/fig4_world_map.png)

Figure 5 presents a horizontal bar chart illustrating the distribution of survey respondents by country of origin.

![text](images/fig5_country_bar.png)

Figure 6 presents the distribution of educational and English proficiency levels.

![text](images/fig6_education_language.png)

Figure 7 presents a heatmap illustrating the cross-tabulation of education and English proficiency levels.

![text](images/fig7_heatmap_edu_english.png)

Figure 8 presents the arrival time of respondents in Syracuse.

![text](images/fig8_arrival_time.png)

Figure 9 presents a bar chart illustrating the Employment sector distribution and time to find a job after arriving in Syracuse.

![text](images/fig9_employment.png)

Figure 10 presents a bar chart illustrating the distribution of job search duration among immigrants.

![text](images/fig10_time_to_find_job.png)

Figure 11 presents a grouped bar chart illustrating the relationship between Education and Time to Find a Job.

![text](images/fig11_english_job.png)

Figure 12 presents the Income distribution of immigrants.

![text](images/fig12_income.png)

Figure 13 presents the relationship between educational attainment and income level among immigrants.

![text](images/fig13_education_income.png)

Figure 14 presents a scatter plot illustrating the relationship between income level and percentage of income spent locally.

![text](images/fig14_income_local.png)

Figure 15 presents a bar chart illustrating the community volunteering activities of immigrants.

![text](images/fig15_volunteering.png)

Figure 16 presents a six-panel histogram illustrating the descriptive statistics including mean, median and standard deviation of the six key quantitative variables analyzed among immigrants.

![text](images/fig16_stats_summary.png)

Figure 17 presents a correlation matrix heatmapillustrating the strength and direction of the six pairwise relationships among the four key economic variables of the survey data.

![text](images/fig17_correlation_matrix.png)

Figure 18 presents the path diagram of the economic integration pathway among immigrants.

![text](images/fig18_path_diagram.png)

[full analysis](Research_Paper.pdf)

