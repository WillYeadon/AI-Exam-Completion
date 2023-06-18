import openai
import re
import pandas as pd
import time

def read_excel_file(file_name):
    return pd.read_excel(file_name, sheet_name=None, engine='openpyxl')

def get_answer(messages, engine_name):
    response = openai.ChatCompletion.create(
        model=engine_name,
        messages=messages,
        temperature=0,
        max_tokens=2000
    )
    answer = response['choices'][0]['message']['content']
    return answer

def check_and_correct_questions(excel_file, openai_api_key):
    openai.api_key = openai_api_key

    messages = [{"role": "system", "content": """
    You are a LaTeX  expert.
    Your task is to carefully examine the following LaTeX enclosed within 
    triple backticks and reformat the questions so that your output will
    compile with no LaTex errors and will have no new lines amid sentences
    but can have new lines to separate equations from sentences or between
    paragraphs. In the event that either no code is supplied or the code is 
    perfectly formatted, output the single word 'OKAY'. Here are some examples
    of input and correct output:

    Input:
    ```
    Rescaling the GPE in terms of units defined by such 
    characteristic scales should yield the following dimensionless equation:

        
    $$

    -\frac{1}{2}\frac{d^{2}\chi(\tilde{x})}{d\tilde{x}^{2}} + U |\chi(\tilde{x})|^{2}\chi(\tilde{x})= \chi(\tilde{x}) ,

    $$ 
    ```
    Correct output:
    Rescaling the GPE in terms of units defined by such characteristic scales should yield the following dimensionless equation:
    $$-\frac{1}{2}\frac{d^{2}\chi(\tilde{x})}{d\tilde{x}^{2}} + U |\chi(\tilde{x})|^{2}\chi(\tilde{x})= \chi(\tilde{x}) ,$$
    
    Input:
    ```
    $\pi^- + p \rightarrow \pi^0 + n$                    
    ```
    Correct output:
    OKAY
    
    Input:
    ```
    Sketch the main physical components of a radio-quiet Active Galactic Nucleus. [5~marks]
    ```
    Correct output:
    OKAY
    
    Input:
    ```
    A beam of coherent light of wavelength $\lambda$ is 
    shone towards a pair of narrow slits 
    separated by 
    distance $d$.
    ```
    Correct output:
    A beam of coherent light of wavelength $\lambda$ is shone towards a pair of narrow slits separated by distance $d$.   
    """}]

    for sheet_name, sheet_data in excel_file.items():
        sheet_data['Checked Questions'] = pd.Series(dtype=str)

        # Wrong file stop
        if 'Question' not in sheet_data.columns:
            continue
    
        for index, response in sheet_data['Cleaned Questions'].iteritems():
            if not pd.isna(response) and pd.isna(sheet_data.get('Checked Questions', pd.Series(dtype=str)).at[index]):
                messages.append({"role": "user", "content": '```' + response + '```'})

                while True:
                    try:
                        corrected_response = get_answer(messages, "gpt-3.5-turbo")
                        sheet_data.at[index, 'Checked Questions'] = corrected_response.strip('`')
                        messages.pop()
                        print(index)
                        break
                    except Exception as e:
                        print(str(e))
                        print("Retrying after a delay due to API error")
                        time.sleep(5)

                # Optionally save the modified Excel file every 10 questions
                #if index % 10 == 0:
                save_excel_file(excel_file, "questions-2020-checked.xlsx")


def save_excel_file(excel_file, file_name):
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        for sheet_name, sheet_data in excel_file.items():
            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

def main():
    file_name = 'questions-2020.xlsx'
    excel_file = read_excel_file(file_name)
    openai_api_key = ""
    check_and_correct_questions(excel_file, openai_api_key)
    save_excel_file(excel_file, "questions-2020-checked.xlsx")

if __name__ == "__main__":
    main()
