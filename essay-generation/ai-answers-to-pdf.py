# This script takes the generated AI answers (and any human answers you have)
# and puts them into anonymized pdfs and creates a secret leger so you can
# find out afterwards which essays were which
#

import random
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
import pandas as pd
import os

def create_pdf_with_reportlab(excel_path, pdf_folder, secret_record, authorship, questions):
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Iterate over the DataFrame to create a PDF for each row
    for index, row in df.iterrows():
        doc_code = f"{os.path.splitext(os.path.basename(excel_path))[0]}-doc-{index + 1}"
        pdf_path = f"{pdf_folder}/{doc_code}.pdf"

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        for question_num, answer in row.items():
            # Handling both string and integer column names
            question_key = str(question_num) if isinstance(question_num, int) else question_num

            if question_key in questions:
                story.append(Paragraph(questions[question_key], styles['Heading2']))
                story.append(Paragraph(str(answer), styles['Normal']))
                story.append(Spacer(1, 12))

                secret_record.append({"Document Code": doc_code, "Authorship": authorship})

        doc.build(story)

def create_pdf_from_excel_single_docs(excel_path, pdf_folder, secret_record, authorship, questions):
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Iterate over the DataFrame to create a PDF for each row
    for index, row in df.iterrows():
        pdf = FPDF()
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)  # Set uni to True for Unicode support
        pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)  # Set uni to True for Unicode support

        # Set the page margins
        pdf.set_margins(10, 10, 10) 

        for question_num, answer in row.items():
            # Handling both string and integer column names
            question_key = str(question_num) if isinstance(question_num, int) else question_num

            # Ensuring question number is valid
            if question_key in questions:
                doc_code = f"{os.path.splitext(os.path.basename(excel_path))[0]}-doc-{index + 1}-{question_key}"
                pdf.add_page()
                pdf.set_font('DejaVu', 'B', 12)
                pdf.multi_cell(0, 10, questions[question_key]) 
                    
                pdf.set_font('DejaVu', '', 12)
                pdf.multi_cell(0, 8, str(answer))  

                secret_record.append({"Document Code": doc_code, "Authorship": authorship})

        # Save the PDF
        pdf_path = f"{pdf_folder}/{doc_code}.pdf"
        pdf.output(pdf_path)

        
questions_23F = {
    "1": "In your experience, is physics based on facts that follow from observations?",
    "2": "What, in your opinion, was the most important advance in natural philosophy between 1100 and 1400?",
    "3": "Was there a scientific revolution in 17th-century Europe?",
    "4": "How did natural philosophers' understanding of electricity change during the 18th and 19th centuries?",
    "5": "Would you judge that Kuhn or Popper gives a more accurate description of physics?"
}

questions_22S = {
    "1": "If most theories have been shown to be false, do we have any reason to have confidence in our theories?",
    "2": "How has scientists’ understanding of charge changed during the 19th and 20th centuries?",
    "3": "Is there a satisfactory interpretation of quantum mechanics?",
    "4": "Was the project to build an atomic bomb typical of science in the twentieth century?",
    "5": "Why should the public believe scientists’ claims?"
}

questions_22F = {
    "1": "Is physics based on facts that follow from observations?",
    "2": "What was the most important advance in natural philosophy between 1100 and 1400?",
    "3": "Was there a scientific revolution in 17th-century Europe?",
    "4": "How did natural philosophers' understanding of electricity change during the 18th and 19th centuries?",
    "5": "Does Kuhn or Popper give a more accurate description of physics?"
}

def main():
    # Paths to your Excel files
    excel_files = ['Human_Answers.xlsx',
                   '22-F_AI_Answers.xlsx',
                   '22-S_AI_Answers.xlsx',
                   '23-F_AI_Answers.xlsx',]

    # Folder for the PDFs
    pdf_folder = "output_folder"
    os.makedirs(pdf_folder, exist_ok=True)

    # Secret record
    secret_record = []

    # Process each Excel file
    for file_path in excel_files:
        authorship = 'AI' if 'AI' in file_path else 'Human'
        questions_dict = questions_22S
        create_pdf_with_reportlab(file_path, pdf_folder, secret_record, authorship, questions_dict)

    # Convert secret record to DataFrame and save
    secret_record_df = pd.DataFrame(secret_record)
    secret_record_path = "leger.xlsx"
    secret_record_df.to_excel(secret_record_path, index=False)

    print(f"PDFs created in folder: {pdf_folder}")
    print(f"Secret record saved at: {secret_record_path}")

    # Shuffle and rename PDFs
    semesters = set(os.path.basename(f).split('_')[0] for f in excel_files)
    updated_secret_record = []

    for semester in semesters:
        pdf_files = [f for f in os.listdir(pdf_folder) if f.startswith(semester)]
        random.shuffle(pdf_files)

        for i, old_name in enumerate(pdf_files):
            new_name = f"{semester}-doc-{i + 1}.pdf"
            os.rename(os.path.join(pdf_folder, old_name), os.path.join(pdf_folder, new_name))

            # Find the corresponding record and update it
            for record in secret_record:
                if record["Document Code"] in old_name:
                    record["Document Code"] = new_name
                    updated_secret_record.append(record)
                    break

    # Save the updated secret record
    updated_secret_record_df = pd.DataFrame(updated_secret_record)
    updated_secret_record_df.to_excel("updated_leger_22S.xlsx", index=False)

    print(f"PDFs created and shuffled in folder: {pdf_folder}")
    print("Updated leger saved.")

if __name__ == "__main__":
    main()