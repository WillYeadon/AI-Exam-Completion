import os
import shutil
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import subprocess

def compile_tex_to_pdf(tex_filename, pdf_filename):
    try:
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, tex_filename], check=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args)
    except subprocess.CalledProcessError:
        print(f"Can't compile {tex_filename}")
        return False
    return True

# Load data from Excel file
df = pd.read_excel('TP3-2019-GPT-4-checked-with-answers.xlsx')

df['Graphics'] = df['Graphics'].fillna(0).astype(int)
df['Retried'] = df['Retried'].fillna(0).astype(int)
df['Available Marks'] = df['Available Marks'].fillna(0).astype(int)

# Group data by Filename
grouped = df.groupby('Filename')

# Initialize Jinja environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.tex')

# Create the output directory if it doesn't exist
output_dir = 'output-tex/'
os.makedirs(output_dir, exist_ok=True)

# Initialize pass and fail counts
passes = 0
fails = 0

# Generate LaTeX documents for each Filename
for filename, group in grouped:
    print(filename)
    data = {'filename': filename, 'rows': group.to_dict('records')}
    latex_doc = template.render(data)
    tex_filename = os.path.join(output_dir, f'{filename}.tex')
    pdf_filename = os.path.join(output_dir, f'{filename}.pdf')
    with open(tex_filename, 'w', encoding='utf-8') as f:
        f.write(latex_doc)

    # Attempt to compile the .tex file to a .pdf file
    if compile_tex_to_pdf(tex_filename, pdf_filename):
        passes += 1
    else:
        fails += 1

# Move files to pass and fail folders or print 'All passed'
if fails == 0:
    print("All passed")
