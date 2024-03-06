import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from scipy.stats import f_oneway, levene

file_path = '../marking-results.xlsx'
xl = pd.ExcelFile(file_path)
scores_by_marker_df = pd.DataFrame()

scores_lists = []
markers = []
means = []
stds = []

custom_colors = ['#8dd3c7', 'gray', '#bebada', '#fb8072', '#80b1d3']

# Loop through each marker sheet, assuming the first sheet is 'True' and the rest are markers
for sheet_name in xl.sheet_names[1:6]:  # Skip the 'True' sheet
    df = xl.parse(sheet_name)
    scores = df['Total'].values
    scores_lists.append(scores)
    markers.append(sheet_name)  # Collect marker names for legend
    means.append(np.mean(scores))  # Calculate and collect the mean
    stds.append(np.std(scores, ddof=1))  # Use ddof=1 for sample standard deviation

# ANOVA test
anova_result = f_oneway(*scores_lists)
print(f"ANOVA result: F={anova_result.statistic:.4f}, p={anova_result.pvalue}")

# Levene's test for homogeneity of variances
levene_result = levene(*scores_lists)
print(f"Levene's test result: W={levene_result.statistic:.4f}, p={levene_result.pvalue}")


fig, ax = plt.subplots(figsize=(10, 6))
n, bins, patches = ax.hist(scores_lists, bins=np.arange(54, 92, 2), stacked=True, color=custom_colors, edgecolor='black')
legend_labels = [f'{marker} (Mean: {mean:.2f})' for marker, mean in zip(markers, means)]

start = 52
for mean, std, color, label in zip(means, stds, custom_colors, legend_labels):
    ax.axvline(mean, color=color, linestyle='--', linewidth=2)
    ax.errorbar(mean, start, xerr=std, fmt='o', color=color, capsize=5)
    start -= 2

ax.legend(legend_labels, title='Marker', loc='center right')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_title('Stacked Distribution of Scores by Markers with Means')
ax.set_xlabel('Total Score')
ax.set_ylabel('Frequency')

bin_edges = np.arange(54, 92, 4)
plt.xticks(bin_edges)
plt.xlim(52,92)
plt.tight_layout(rect=[0, 0, 0.85, 1]) 
plt.savefig('stacked-scores-by-marker.png', dpi=300)
plt.show()

