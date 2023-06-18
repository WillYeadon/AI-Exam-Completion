import openai
import pandas as pd
import re
import time
import subprocess
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import BpeTrainer
from pylatexenc.latexwalker import LatexWalker, LatexWalkerError
from jinja2 import Environment, FileSystemLoader

def is_valid_answer(answer):
    # Check for excessive whitespace
    whitespace_ratio = len(re.findall(r'\s', answer)) / len(answer)
    if whitespace_ratio > 0.5:
        return False

    # Check for repeated characters
    repeated_chars = re.findall(r'(.)\1{4,}', answer)
    if repeated_chars:
        return False

    return True
def remove_excessive_whitespace(answer):
    # Remove excessive spaces, tabs, or newlines
    cleaned_answer = re.sub(r'\s{2,}', ' ', answer)

    return cleaned_answer


def count_tokens(messages):
    total_tokens = 0
    for message in messages:
        total_tokens += len(tokenizer.encode(message['content']).tokens)
    return total_tokens

def test_latex_compilation(answer):
    test_template = r"""
    \documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{amsmath}
    \usepackage{amssymb}
    \usepackage{graphicx}
    \usepackage{enumitem}
    \usepackage{lipsum}
    \usepackage{hyperref}
    \usepackage[T1]{fontenc}
    \usepackage{geometry}
    \usepackage{braket}
    \geometry{a4paper, left=5mm, top=20mm, right=5mm, bottom=20mm}   
    \hfuzz=\maxdimen
    \begin{document}
    {{ answer }}
    \end{document}
    """

    env = Environment(loader=FileSystemLoader('.'))
    template = env.from_string(test_template)
    latex_doc = template.render(answer=answer)

    with open("temp_test.tex", "w", encoding="utf-8") as f:
        f.write(latex_doc)

    result = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', '.', 'temp_test.tex'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Compilation error:")
        print(result.stderr)
        return False
    return True

def remove_image_references(text):
    return re.sub(r'\n?!?\[.*?\]\(attachment:.*?\.(?:png|jpg|jpeg|gif|bmp)\)', '', text)

def is_valid_latex(latex_str):
    try:
        LatexWalker(latex_str).get_latex_nodes()
        return True
    except LatexWalkerError:
        return False

def truncate_invalid_latex(latex_str, max_chars=None):
    if max_chars is not None:
        latex_str = latex_str[:max_chars]
    last_command = list(re.finditer(r'\\(?:[a-zA-Z]+|.)', latex_str))[-1]
    return latex_str[:last_command.start()]

def get_answer(messages, engine_name):
    try:
        # Calculate the remaining tokens for the answer
        tokens_used = count_tokens(messages)
        tokens_available = 4096 - tokens_used

        response = openai.ChatCompletion.create(
            model=engine_name,
            messages=messages,
            temperature=0,
            max_tokens=min(2000, tokens_available - 1)  # Set max_tokens to the smaller of 2000 or the remaining tokens
        )
        answer = response['choices'][0]['message']['content']

        return answer
    except openai.OpenAIError as e:
        error_msg = str(e)
        # Check if the error message starts with the maximum context length error
        if error_msg.startswith("This model's maximum context length"):
            return "MESSAGE OVERFLOW"
        else:
            # Raise an exception for other API errors
            raise Exception("API Error: " + error_msg)

# Initialize the tokenizer
tokenizer = Tokenizer(BPE())
tokenizer.pre_tokenizer = Whitespace()
tokenizer.train_from_iterator(["dummy text"], trainer=BpeTrainer(vocab_size=50000))

# Set up the OpenAI API
openai.api_key = ""

# Load the Excel workbook
df = pd.read_excel("questions-2020-checked-marks.xlsx")

used_packages = set()
preamble = ""
max_retries = 3

for row in range(len(df)):
    print('Row', row)
    filename = df.loc[row, 'Filename']
    question = df.loc[row, 'Checked Questions']
    question_number = df.loc[row, 'Question Number']
    existing_response = df.loc[row, 'Responses']

    # Check for optional preamble
    if re.match(r'^Q\d+[a-z]+$', question_number):
        preamble = question

    # Concatenate preamble with sub-questions if necessary
    if re.match(r'^Q\d+[a-z]+\w+$', question_number) and isinstance(preamble, str):
        question = preamble + ' ' + question

    if pd.notna(question) and pd.isna(existing_response) and question.strip():
        messages = [
            {"role": "system", "content": "You are a Physics professor."},
            {"role": "system", "content": "Answer the question between triple backticks, showing your work step by step."},
            {"role": "system", "content": "IMPORTANT: Use Latex code for equations and numbers. Please define any custom LaTeX commands you use in your answer."},
            {"role": "system", "content": "IMPORTANT: Ensure numbers and units in the text are properly formatted using LaTeX, e.g., use `$10^24 cm^{-2}$` instead of '10^24 cm^-2'."},
            {"role": "system", "content": "IMPORTANT: Do not attempt to draw sketches or images. Do not include figures"},
            {"role": "system", "content": "IMPORTANT: Limit your answers to a maximum of 6000 characters (approx. 1500 tokens)."},
            {"role": "user", "content": '' + str(question) + ''},
        ]

        retries = 0
        while retries < max_retries:
            try:
                answer_gpt_35_turbo = get_answer(messages, "gpt-3.5-turbo")
                answer_gpt_35_turbo = remove_image_references(answer_gpt_35_turbo)
                              
                if not is_valid_answer(answer_gpt_35_turbo):
                    # Remove excessive whitespace
                    answer_gpt_35_turbo = remove_excessive_whitespace(answer_gpt_35_turbo)
                    
                    # Send the message back to the API to correct the formatting
                    messages.append({"role": "system", "content": "IMPORTANT: That previous response was poorly formatted. Please try toa answer the question again more concisely sending the corrected version as a new message"})
                    #messages.append({"role": "user", "content": answer_gpt_35_turbo})  # Add the corrected answer as a new user message
                    retries += 1
                    continue

                if not test_latex_compilation(answer_gpt_35_turbo):
                    # Send the message back to the API to correct LaTeX formatting
                    messages.append({"role": "system", "content": "IMPORTANT: Latex compilation failed on your response. Please correct the LaTeX formatting in your previous response sending the corrected version as a new message."})
                    #messages.append({"role": "user", "content": answer_gpt_35_turbo})  # Add the corrected answer as a new user message
                    retries += 1
                    continue

        
                # Extract and remove \usepackage commands
                packages = re.findall(r'\\usepackage\{[a-zA-Z0-9_-]+\}', answer_gpt_35_turbo)
                used_packages.update(packages)
                answer_gpt_35_turbo = re.sub(r'\\usepackage\{[a-zA-Z0-9_-]+\}', '', answer_gpt_35_turbo)
        
                df.loc[row, 'Responses'] = answer_gpt_35_turbo
                break
            except Exception as e:
                print(str(e))
                print("Retrying after a delay due to API error")
                time.sleep(5)

        if retries == max_retries:
            df.loc[row, 'Responses'] = 'Compilation failed'
            print(f"Compilation failed for row {row}")

        # Add a new column 'Retried' and set its value to 1 if retries > 0, else 0
        df.loc[row, 'Retried'] = 1 if retries > 0 else 0

        df.to_excel("questions_with_answers_2022-2018.xlsx", index=False)
    else:
        print(f"Skipping row {row} as response already exists")


#### New Regex
# Extract the year and filename using regex
df['Year'] = df['Filename'].str.extract(r'(\d+)-papers-raw\\(.+?)~Q\d+\.tex')
# Replace any backslashes with hyphens and concatenate the year and filename
df['Filename'] = df['Year'] + '-' + df['Filename'].str.replace(r'\\', '')
# Remove the unnecessary parts from the filename
df['Filename'] = df['Filename'].str.extract(r'(\d+-\w+(?:\s\w+)*)')

# Save the updated DataFrame to the questions_with_answers.xlsx file
df.to_excel("questions_with_answers_2020.xlsx", index=False)

print("\nPackages used:")
for package in used_packages:
    print(package)
