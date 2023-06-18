import re
import pandas as pd

def update_question_number(question_number, last_used_letter):
    if re.search(r'[a-h]', question_number):
        last_used_letter = re.search(r'[a-h]', question_number).group()

    if last_used_letter and re.search(r'Q\d+[i]+$', question_number):
        question_number += last_used_letter

    match = re.match(r'(Q\d+)([a-h]?)([i]+)?([a-h]?)', question_number)
    if match:
        final_question_number = match.group(1) + match.group(4) + match.group(2) + (match.group(3) or '')
        return final_question_number, last_used_letter
    else:
        return question_number, last_used_letter

def update_question_numbers_in_dataframe(df):
    last_used_letter = None
    for index, row in df.iterrows():
        question_number = row['Question Number']
        updated_question_number, last_used_letter = update_question_number(question_number, last_used_letter)
        df.at[index, 'Question Number'] = updated_question_number

    return df

# Read the Excel file
file_name = 'questions-2020-checked.xlsx'
df = pd.read_excel(file_name)

# Update the question numbers in the 'Question Number' column
updated_df = update_question_numbers_in_dataframe(df)

# Save the updated DataFrame back to the same Excel file
updated_df.to_excel(file_name, index=False, engine='openpyxl')
