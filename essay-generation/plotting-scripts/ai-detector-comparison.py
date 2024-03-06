import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

percentage_df = pd.read_excel('../computational-AI-detection.xlsx', sheet_name='percentage')

# Splitting the dataset into AI and Human based on the 'Actual' column
ai_authored_df = percentage_df[percentage_df['Actual'] == 100]
human_authored_df = percentage_df[percentage_df['Actual'] == 0]

# Calculate average percentage predictions for AI and Human for each detector
ai_averages = ai_authored_df.iloc[:, 2:].mean()
human_averages = human_authored_df.iloc[:, 2:].mean()

# Colours
colors = ['#E76F51', '#2A9D8F']

fig, ax = plt.subplots(figsize=(10, 6))
width = 0.35       
r1 = np.arange(len(ai_averages))
r2 = [x + width for x in r1]
ax.bar(r1, ai_averages, color=colors[0], width=width, alpha = 1, edgecolor='black', label='AI Authored')
ax.bar(r2, human_averages, color=colors[1], width=width, alpha = 1, edgecolor='black', label='Human Authored')

ax.set_xlabel('Detectors', size=15)
ax.set_ylabel('Average Percentage AI Prediction', size=15)
ax.set_xticks([r + width/2 for r in range(len(ai_averages))])
ax.set_xticklabels(ai_averages.index, rotation=0, size=14)
ax.set_title('Average Percentage Predictions for AI and Human Authored Work by Detector',
             size=15)
ax.legend()

plt.tight_layout()
plt.savefig('AI-detectors.png', dpi=300)
plt.show()

# Binary predictions
binary_df = pd.read_excel('../computational-AI-detection.xlsx', sheet_name='binary')

# Calculate TP, FP, TN, FN, Accuracy, and Precision
results = []

for detector in binary_df.columns[2:]: 
    cm = confusion_matrix(binary_df['Actual'], binary_df[detector], labels=[1, 0])
    TP, FN, FP, TN = cm.ravel()
    accuracy = (TP + TN) / (TP + FP + TN + FN)
    precision = TP / (TP + FP) if TP + FP > 0 else 0
    results.append((detector, TP, FP, TN, FN, accuracy, precision))

print("Detector\t\tTP\tFP\tTN\tFN\tAccuracy\tPrecision")
for result in results:
    print(f"{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}\t{result[4]}\t{result[5]:.2f}\t\t{result[6]:.2f}")

