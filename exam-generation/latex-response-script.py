import openai
import re
import pandas as pd
import time

# Load the Excel workbook
file_name = 'TP3-2019-GPT-4-checked-with-answers.xlsx'
excel_file = pd.read_excel(file_name, sheet_name=None, engine='openpyxl')

# Regular expressions to match LaTeX \includegraphics blocks and the remaining case
pattern_includegraphics = re.compile(r'\\begin{center}\s*(?:\\vskip[^\\]*\s*)?\\includegraphics[^{]*{[^}]*}\s*(?:\\vskip[^\\]*\s*)?\\end{center}')
pattern_remaining = re.compile(r'(?:\\vskip[^\\]*\s*)?\\end{center}')

# Iterate through sheets and cells
for sheet_name, sheet_data in excel_file.items():
    for col_name in sheet_data.columns:
        for index, value in enumerate(sheet_data[col_name]):
            if value is not None and isinstance(value, str):
                # Remove the matched LaTeX text (first pass)
                value = pattern_includegraphics.sub('', value)
                # Remove the remaining LaTeX text (second pass)
                sheet_data.at[index, col_name] = pattern_remaining.sub('', value)

# Save the modified Excel file
with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    for sheet_name, sheet_data in excel_file.items():
        sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

# Function to get answer from OpenAI API
def get_answer(messages, engine_name):
    response = openai.ChatCompletion.create(
        model=engine_name,
        messages=messages,
        temperature=0,
        max_tokens=2000
    )
    answer = response['choices'][0]['message']['content']
    return answer

openai.api_key = ""

# System message
messages = [{"role": "system", "content": """
            You are a LaTeX  expert.
            Your task is to carefully examine the following LaTeX code 
            enclosed within triple backticks and return either a corrected 
            version (if there are any mistakes) or the origional version. 
            
            Always return the LaTeX code, never a statement about the 
            correctness of the code. Below are two examples showing a 
            correct reponsea and an incorrect response for two inputs
            
            Example 1:
            Input: ```$\alpha = m \omega$```
            Correct Response: '$\alpha = m \omega$'
            Incorrect Response: 'The code is correct' 
            
            Example 2:
            Input: ```\beta = 10$```
            Correct Response: '$\beta = 10$'
            Incorrect Response: 'The code is incorrect, you need to add a $' 
            
            Please review and correct the following LaTeX code if necessary:
"""}]

# Iterate through sheets and add a new 'Checked' column
for sheet_name, sheet_data in excel_file.items():
    # Create a new 'Checked' column with NaN values
    sheet_data['Checked Answer'] = pd.Series(dtype=str)
    
    for index, response in sheet_data['Responses'].iteritems():
        if not pd.isna(response) and pd.isna(sheet_data.at[index, 'Checked Answer']):
            # Add the response to the messages
            messages.append({"role": "user", "content": '```' + response + '```'})
            
            # Continuously try to get the corrected response from the OpenAI API
            while True:
                try:
                    corrected_response = get_answer(messages, "gpt-3.5-turbo")
                    break
                except Exception as e:
                    print(str(e))
                    print("Retrying after a delay due to API error")
                    time.sleep(5)
    
            # Store the corrected response in the 'Checked' column
            sheet_data.at[index, 'Checked Answer'] = corrected_response.strip('`')
    
            # Save the modified Excel file after each iteration
            with pd.ExcelWriter("questions_with_answers_checked.xlsx", engine='openpyxl') as writer:
                for sheet_name, sheet_data in excel_file.items():
                    sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
    
            # Remove the user message to prepare for the next iteration
            messages.pop()
            print(index)

# Save the modified Excel file
with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    for sheet_name, sheet_data in excel_file.items():
        sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
