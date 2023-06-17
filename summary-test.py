import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

xl = pd.ExcelFile('summary-stats.xlsx')
df = xl.parse('All')
df_melted = df.melt(id_vars='Exam', value_vars=['GPT-3', 'GPT-3 !0', 'GPT-4', 'GPT-4 !0'], var_name='Model', value_name='Score')

palette = {
    "GPT-3": "#3498db",   # Blue color for GPT-3
    "GPT-4": "#e74c3c",   # Red color for GPT-4
    "GPT-3 !0": "#2ecc71", # Green color for GPT-3 !0
    "GPT-4 !0": "#f1c40f"  # Yellow color for GPT-4 !0
}

# First plot for 'GPT-3' and 'GPT-4'
df_melted1 = df_melted[df_melted['Model'].isin(['GPT-3', 'GPT-4'])]
sns.barplot(x='Exam', y='Score', hue='Model', data=df_melted1, palette=palette)

plt.title('Scores by Exam and Model (GPT-3 and GPT-4)')
plt.ylim(0, 100)  # set y axis limits
plt.axhline(y=40, color='black', linestyle='--')  # add dashed line at y = 40
plt.legend(loc='upper right')  # move legend to upper right
plt.xticks(rotation=45)  # rotate x-axis labels

plt.tight_layout()  # adjust spacing
plt.savefig('summary1.png', dpi=300) 
plt.show()

# Second plot for 'GPT-3 !0' and 'GPT-4 !0'
df_melted2 = df_melted[df_melted['Model'].isin(['GPT-3 !0', 'GPT-4 !0'])]
sns.barplot(x='Exam', y='Score', hue='Model', data=df_melted2, palette=palette)

plt.title('Scores by Exam and Model (GPT-3 !0 and GPT-4 !0)')
plt.ylim(0, 100)  # set y axis limits
plt.axhline(y=40, color='black', linestyle='--')  # add dashed line at y = 40
plt.legend(loc='upper center')  # move legend to upper right
plt.xticks(rotation=45)  # rotate x-axis labels

plt.tight_layout()  # adjust spacing
plt.savefig('summary2.png', dpi=300) 
plt.show()
