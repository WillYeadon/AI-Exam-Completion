# Simple script to send in a list of prompts and record the responces
#
# -*- coding: utf-8 -*-
import openai
import pandas as pd
from openai import OpenAI

# Use your OpenAI API key
openai_api_key = "YOUR-KEY"

def generate_ai_answer(prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
        max_tokens=750  
    )
    ai_answer = response.choices[0].message.content.replace("\n", " ")
    return ai_answer

def load_prompts_from_file(file_path):
    # Load prompts from a CSV file with UTF-8 encoding
    df = pd.read_csv(file_path, encoding='utf-8')
    prompts = {}
    for _, row in df.iterrows():
        category = row["Category"]
        question = row["Question"]
        prompt = row["Prompt"]

        if category not in prompts:
            prompts[category] = {}
        if question not in prompts[category]:
            prompts[category][question] = []

        prompts[category][question].append(prompt)
    return prompts

def main():
    file_path = "prompts.csv"  # Ensure this file is UTF-8 encoded

    prompts_by_category = load_prompts_from_file(file_path)

    for category, questions in prompts_by_category.items():
        responses = {question: [] for question in questions}
        for question, question_prompts in questions.items():
            for prompt in question_prompts:
                ai_answer = generate_ai_answer(prompt)
                responses[question].append(ai_answer)

        # Convert to DataFrame and Export to Excel
        df = pd.DataFrame(responses)
        df.to_excel(f"{category}_AI_Answers.xlsx", index=False)

if __name__ == "__main__":
    main()
