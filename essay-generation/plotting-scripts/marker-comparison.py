import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from matplotlib.ticker import MaxNLocator
from scipy.stats import chi2_contingency, ttest_1samp
from scipy.stats import linregress

# Define a function to convert Likert scale responses to a numerical scale
def convert_likert_to_scale(response):
    scale = {
        '1 - Definitely human': 1,
        '2 - Probably human': 2,
        '3 - Probably AI': 3,
        '4 - Definitely AI': 4
    }
    return scale.get(response, None)


def marker_consistency(df):
    return df['Binary_Score'].value_counts()

def calculate_accuracy(df):
    return (df['Binary_Score'] == true_authorship['Authorship']).mean()

file_path = '../marking-results.xlsx'
colors = ['#E76F51', '#2A9D8F']  

xl = pd.ExcelFile(file_path)
sheet_names = xl.sheet_names

true_authorship = xl.parse('True')
marker_1 = xl.parse('Marker #1')
marker_2 = xl.parse('Marker #2')
marker_3 = xl.parse('Marker #3')
marker_4 = xl.parse('Marker #4')
marker_5 = xl.parse('Marker #5')

# Convert AI identification responses to numerical scale for each marker
for df in [marker_1, marker_2, marker_3, marker_4, marker_5]:
    df['AI_Score'] = df['AI?'].apply(convert_likert_to_scale)

# Merge the markers' scores with the true authorship
# First, make sure the document codes are consistent
true_authorship['Document Code'] = true_authorship['Document Code'].str.strip('.pdf')
for df in [marker_1, marker_2, marker_3, marker_4, marker_5]:
    df['Candidate'] = df['Candidate'].str.strip('.pdf')

# Now merge
merged_data = pd.DataFrame()
for df in [marker_1, marker_2, marker_3, marker_4, marker_5]:
    merged = df[['Candidate', 'AI_Score']].merge(true_authorship, left_on='Candidate', right_on='Document Code', how='left')
    merged_data = pd.concat([merged_data, merged])

# Plot the distribution of AI identification scores with stacking
fig, ax = plt.subplots(figsize=(7, 5))

# Prepare data for stacking
scores = []
labels = []
for actual_type, group in merged_data.groupby('Authorship'):
    scores.append(group['AI_Score'])
    labels.append(str(actual_type))

# Use the `stacked=True` parameter to stack the histograms
ax.hist(scores, bins=4, range=(0.5, 4.5), color=colors,
        stacked=True, alpha=1, label=labels, edgecolor='black')

ax.yaxis.set_major_locator(MaxNLocator(integer=True))

ax.set_title('Distribution of AI Identification Scores')
ax.set_xlabel('AI Identification Score')
ax.set_ylabel('Count')
ax.set_xticks(range(1, 5))
ax.set_xticklabels(['Definitely human', 'Probably human', 'Probably AI', 'Definitely AI'])
ax.legend(title='Actual Type')
plt.savefig('all-ID.png', dpi=300)
plt.show()

contingency_table = pd.crosstab(merged_data['Authorship'], merged_data['AI_Score'])

chi2, p_value, dof, expected = chi2_contingency(contingency_table)
print(contingency_table)
print(f"Chi-square Statistic: {chi2}, P-value: {p_value}")

# Analyze deviation from 25% for each category
expected_proportion = 0.25
observed_proportions = merged_data['AI_Score'].value_counts(normalize=True)
deviation_from_random = observed_proportions - expected_proportion
print("Deviation from random (25% in each category):")
print(deviation_from_random)

# Collapsing the Likert scale to binary and analyzing
merged_data['Binary_Score'] = merged_data['AI_Score'].apply(lambda x: 'AI' if x > 2 else 'Human')
binary_expected_proportion = 0.5
binary_observed_proportions = merged_data['Binary_Score'].value_counts(normalize=True)
binary_deviation_from_random = binary_observed_proportions - binary_expected_proportion
print("\nBinary deviation from random (50/50):")
print(binary_deviation_from_random)

marker_1['Binary_Score'] = marker_1['AI_Score'].apply(lambda x: 'AI' if x > 2 else 'Human')
marker_2['Binary_Score'] = marker_2['AI_Score'].apply(lambda x: 'AI' if x > 2 else 'Human')
marker_3['Binary_Score'] = marker_3['AI_Score'].apply(lambda x: 'AI' if x > 2 else 'Human')
marker_4['Binary_Score'] = marker_4['AI_Score'].apply(lambda x: 'AI' if x > 2 else 'Human')
marker_5['Binary_Score'] = marker_5['AI_Score'].apply(lambda x: 'AI' if x > 2 else 'Human')

marker_accuracy = {
    'One': calculate_accuracy(marker_1),
    'Two': calculate_accuracy(marker_2),
    'Three': calculate_accuracy(marker_3),
    'Four': calculate_accuracy(marker_4),
    'Five': calculate_accuracy(marker_5),
}

print("\nMarker Accuracy Rates:")
for marker, accuracy in marker_accuracy.items():
    print(f"{marker}: {accuracy:.2f}")


print("\nMarker Consistency (AI vs. Human guesses):")
for marker_df in [marker_1, marker_2, marker_3, marker_4, marker_5]:
    consistency = marker_consistency(marker_df)
    print(consistency)
    
# Our contingency table
data = np.array([
    [36, 37, 35, 42],  # AI
    [59, 39, 32, 20]   # Human
])

proportions = data / data.sum(axis=0)
scores = np.array([1, 2, 3, 4])

trend_tests = [linregress(scores, prop) for prop in proportions]
trend_pvalues = [test.pvalue for test in trend_tests]
trend_statistics = [test.slope for test in trend_tests]

print(trend_pvalues, trend_statistics)



