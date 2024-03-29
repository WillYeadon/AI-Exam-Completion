import openai
import matplotlib.pyplot as plt
import numpy as np
import io
import os
import re
import threading
import concurrent.futures

openai_api_key = ""

def preprocess_code(ai_code):
    # Remove Markdown code block syntax
    cleaned_code = re.sub(r'```python|```', '', ai_code)
    # Remove LaTeX or similar non-Python syntax
    cleaned_code = re.sub(r'\$\$.*?\$\$', '', cleaned_code, flags=re.DOTALL)

    # Find the start of the Python code (first import statement)
    start_idx = cleaned_code.find('import ')
    if start_idx == -1:
        start_idx = 0  # If no import, start from the beginning

    # Find the end of the Python code ('plt.show()')
    end_idx = cleaned_code.rfind('plt.show()')
    if end_idx != -1:
        end_idx += len('plt.show()')  # Include 'plt.show()' in the extracted code

    # Extract and return the relevant part of the code
    return cleaned_code[start_idx:end_idx]

def generate_ai_answer(client, prompt, model_name):
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "system", "content": prompt}],
        temperature=1,
        max_tokens=2000
    )
    return response.choices[0].message.content.strip(), model_name

def execute_code(code):
    try:
        namespace = {'plt': plt, 'np': np, 'numpy': np}
        if 'plt.show()' in code:
            code = code.replace('plt.show()', '')
            exec(code, namespace)
            fig = plt.gcf()
            plt.close('all')
            return fig
        else:
            exec(code, namespace)
            fig = plt.gcf()
            plt.close('all')
            return fig if fig.get_axes() else None
    except Exception as e:
        print(f"Error executing code: {e}")
        return None

def execute_code_with_timeout(code, timeout=30):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(execute_code, code)
        try:
            result = future.result(timeout=timeout)
            return result
        except concurrent.futures.TimeoutError:
            print("Code execution timed out")
            return None
    
def process_script(file_path, client, attempt_number, model_name):
    with open(file_path, 'r') as file:
        script_lines = file.readlines()
    plot_task_description = ""
    for line in script_lines:
        if line.strip().startswith("#"):
            plot_task_description += line.strip("# ").strip() + " "

    prompt = f"{plot_task_description}"
    ai_code, used_model = generate_ai_answer(client, prompt, model_name)
    cleaned_ai_code = preprocess_code(ai_code)

#    if used_model == "gpt-4-1106-preview":# or used_model == "gpt-3.5-turbo":
#    if '```python' in ai_code:
#        try:
#            ai_code = ai_code.split("```python\n")[1].split("\n```")[0]
#        except IndexError:
#            print("Error: Could not extract code from the AI response.")
#            return
#    print(f"Generated code for task:\n{ai_code}\n")
#    fig = execute_code_with_timeout(ai_code)
    print(f"Processed code for task:\n{cleaned_ai_code}\n")
    fig = execute_code_with_timeout(cleaned_ai_code)
    if fig and fig.get_axes():
        assignment_name = os.path.splitext(os.path.basename(file_path))[0]
        assignment_folder = os.path.join('4-ai-images-folders', assignment_name)
        os.makedirs(assignment_folder, exist_ok=True)
        plot_filename = os.path.join(assignment_folder, assignment_name + f'_attempt_{attempt_number}.png')
        fig.savefig(plot_filename)
        print(f"Plot saved in {plot_filename}")
    else:
        print("No valid plot generated for this task.")

def main():
    script_files = ['Assignment-1.py', 'Assignment-2.py', 'Assignment-3.py',
                    'Assignment-4-a.py', 'Assignment-4-b.py', 'Assignment-5-a.py',
                    'Assignment-5-b.py', 'Assignment-6-a.py', 'Assignment-6-b.py',
                    'Assignment-7-a.py', 'Assignment-7-b.py', 'Assignment-8-a.py',
                    'Assignment-8-b.py', 'Assignment-8-c.py']
    script_folder = 'assignment-python-scripts'
#    script_folder = 'assignment-python-scripts'
    os.makedirs('ai-images-folders', exist_ok=True)

    client = openai.OpenAI(api_key=openai_api_key)
    print('Connected')

    max_attempts_per_file = 25  # Maximum attempts for each file to avoid infinite loops
    required_examples = 5  # Required examples per file

    for script_file in script_files:
        file_path = os.path.join(script_folder, script_file)
        assignment_name = os.path.splitext(os.path.basename(file_path))[0]
        assignment_folder = os.path.join('ai-images-folders', assignment_name)
        os.makedirs(assignment_folder, exist_ok=True)

        # Check existing number of plots
        existing_plots = len([f for f in os.listdir(assignment_folder) if f.endswith('.png')])
        if existing_plots >= required_examples:
            print(f"Already have {existing_plots} plots for {assignment_name}, skipping.")
            continue

        attempt = 1
        successful_attempts = existing_plots

        while successful_attempts < required_examples and attempt <= max_attempts_per_file:
            prev_successful_attempts = successful_attempts

            process_script(file_path, client, attempt, model_name="gpt-4-1106-preview")
            successful_attempts = len([f for f in os.listdir(assignment_folder) if f.endswith('.png')])
            
            # Break if no new successful attempt is made
            if successful_attempts == prev_successful_attempts:
                print(f"No new plot generated for {assignment_name} on attempt {attempt}.")
             
#            process_script(file_path, client, attempt, "gpt-4-1106-preview")
            attempt += 1

if __name__ == "__main__":
    main()