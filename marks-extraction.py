import pandas as pd
import re

# Load the Excel file
file_name = "2022-2018-checked-questions-only.xlsx"
df = pd.read_excel(file_name, engine="openpyxl")

# Function to extract marks
def extract_marks(cell):
    cell_str = str(cell)
    if len(cell_str) == 0:
        return ''
    matches = re.findall(r"\[(\d+)[ ~]*mar?ks\]", cell_str)
    if matches:
        return sum(map(int, matches))
    else:
        return 0


# Apply the function to the 'Checked Questions' column
df["Marks"] = df["Cleaned Questions"].apply(extract_marks)
#df["Marks"] = df["Cleaned Questions"].apply(extract_marks)

# Save the updated DataFrame to a new Excel file
df.to_excel("cleaned_2022-2018-checked-questions-only.xlsx", index=False, engine="openpyxl")
