import re
import pandas as pd

def clean_question(question):
    if not isinstance(question, str):
        return question

    # Remove comments
    question = re.sub(r'%.*', '', question)
    # Remove document, itemize, and usepackage related commands
    question = re.sub(r'\\(documentclass|begin|end|usepackage|setlength|large|hsize|leftskip|vskip|noindent).*', '', question)
    # Remove \item and strike action messages
    question = re.sub(r'\\item\[\(.*\)\]|(\[This (sub-)?question has been deleted as a result of strike action.\])', '', question)
    # Remove \includegraphics
    question = re.sub(r'\\includegraphics.*', '', question)
    # Remove curly braces at the beginning and end of the question
    question = re.sub(r'^\{|\}$', '', question)
    # Remove extra newlines and whitespace
    question = re.sub(r'\n\s*\n', '\n', question).strip()
    
    return question




# Load your Excel file
df = pd.read_excel("TP3-2019-GPT-4.xlsx")
df['Question'] = df['Question'].str.replace('_x000D_', '\n')

# Clean the questions
df['Cleaned Questions'] = df['Question'].apply(clean_question)

# Save the cleaned questions back to the Excel file
df.to_excel("TP3-2019-GPT-4.xlsx", index=False)
