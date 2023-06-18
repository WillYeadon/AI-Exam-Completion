import re
import pandas as pd
import os

def extract_questions(content):
    content = re.sub(r'\\begin{itemize}|\\end{itemize}', '', content)
    question_pattern = re.compile(r'\\item\[\((.*?)\)\]\s*((?:.*?\n?)+?)(?=(?:\\item|$))', re.DOTALL)
    questions = [(match.group(1), match.group(2).strip()) for match in question_pattern.finditer(content + '\\item')]
    return questions

def extract_preamble(content):
    preamble = re.search(r'^(.+?)\\begin{itemize}', content, flags=re.DOTALL)
    return preamble.group(1).strip() if preamble else ''

def extract_question_number_from_filename(filename):
    return re.search(r'~(Q\d+)\.tex', filename).group(1)

directory = 'example-raw-tex/2020'
tex_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.tex')]


data = {'Filename': [],
        'Question Number': [],
        'Graphics': [],
        'Question': [],
        'Responses': []}

for tex_file in tex_files:
    with open(tex_file, 'rb') as f:
        content = f.read().decode('utf-8')

    questions = extract_questions(content)
    preamble = extract_preamble(content)
    question_number_prefix = extract_question_number_from_filename(tex_file)

    for i in range(len(questions)):
        graphics = '1' if '\\includegraphics' in questions[i][1] else '0'

        question_number = question_number_prefix + questions[i][0]
        
        # Add the preamble to the first question
        question_text = questions[i][1].strip()
        if i == 0:
            question_text = preamble.strip() + '\n\n' + question_text

        data['Filename'].append(tex_file)
        data['Question Number'].append(question_number)
        data['Graphics'].append(graphics)
        data['Question'].append(question_text.strip())  # Strip leading and trailing newlines
        data['Responses'].append("")

df = pd.DataFrame(data)
df.to_excel('questions-2020.xlsx', index=False)
