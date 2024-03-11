import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from matplotlib.ticker import MaxNLocator
from scipy.stats import ttest_ind
from scipy.stats import norm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

file_path = '../marking-results.xlsx'
colors = ['#E76F51', '#2A9D8F'] 

xl = pd.ExcelFile(file_path)
true_authorship = xl.parse('True')
marker_1 = xl.parse('Marker #1')
marker_2 = xl.parse('Marker #2')
marker_3 = xl.parse('Marker #3')
marker_4 = xl.parse('Marker #4')
marker_5 = xl.parse('Marker #5')

scores_data = pd.DataFrame()
for df in [marker_1, marker_2, marker_3, marker_4, marker_5]:
    df_merged = df[['Candidate', 'Total']].merge(true_authorship, left_on='Candidate', right_on='Document Code', how='left')
    scores_data = pd.concat([scores_data, df_merged])

fig, ax = plt.subplots(figsize=(7, 5))
human_scores = scores_data[scores_data['Authorship'] == 'Human']['Total']
ai_scores = scores_data[scores_data['Authorship'] == 'AI']['Total']

bins = range(int(scores_data['Total'].min()), int(scores_data['Total'].max()) + 2, 2)
ax.hist([ai_scores, human_scores], bins=bins, stacked=True, color=colors, label=['AI', 'Human'], edgecolor='black')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))

mean_human = human_scores.mean()
mean_ai = ai_scores.mean()
sd_human = human_scores.std()
sd_ai = ai_scores.std()
se_human = round(sd_human/np.sqrt(150),1)
se_ai = round(sd_ai/np.sqrt(150),1)

print('Human: ', mean_human, sd_human)
print('AI: ', mean_ai, sd_ai)

vlines = ['#217d72', '#b85840'] # green then red
ax.vlines(mean_human, 0, human_scores.count(), color=vlines[0], linestyle='--', label=f'Human Avg: {mean_human:.2f}')
ax.vlines(mean_ai, 0, ai_scores.count(), color=vlines[1], linestyle='--', label=f'AI Avg: {mean_ai:.2f}')

y_pos_human = 52
y_pos_ai = 55

ax.errorbar(mean_human, y_pos_human, xerr=se_human, fmt='o', color=colors[1], capsize=5)
ax.errorbar(mean_ai, y_pos_ai, xerr=se_ai, fmt='o', color=colors[0], capsize=5)
ax.legend(title='Type', loc='upper right', fontsize='small', 
          labels=['Human', 'AI', f'Human Avg: {mean_human:.2f} (SD: {sd_human:.2f})', f'AI Avg: {mean_ai:.2f} (SD: {sd_ai:.2f})'])

legend_elements = [
    Patch(facecolor='#E76F51', edgecolor='black', label='AI'),
    Patch(facecolor='#2A9D8F', edgecolor='black', label='Human'),
    Line2D([0], [0], color='#b85840', lw=2, linestyle='--', label=f'AI Avg: {mean_ai:.1f} (SE: {se_ai})'),
    Line2D([0], [0], color='#217d72', lw=2, linestyle='--', label=f'Human Avg: {mean_human:.1f} (SE: {se_human})')
]

ax.legend(handles=legend_elements, title='Type', loc='upper right', fontsize='small')
ax.set_title('Stacked Distribution of Scores by Type')
ax.set_xlabel('Essay Score')
ax.set_ylabel('Count')
ax.set_ylim(0,60)

bin_edges = np.arange(54, 92, 4)

plt.xticks(bin_edges)
plt.xlim(52,92)
plt.tight_layout()  # Adjust layout to make room for the legend
plt.savefig('all-scores.png', dpi=300)
plt.show()

ttest_results = {
    'Metric': ['Means'],
    'P-value': [
        ttest_ind(human_scores, ai_scores).pvalue,
    ]
}

ttest_results_df = pd.DataFrame(ttest_results)
print("T-Test Results for Comparing Human and AI Essays:\n")
print(ttest_results_df.to_string(index=False))

print('Cumulative probability of a z-score for X = 60:', 100*(1 - norm.cdf((60 - mean_ai) / sd_ai)))