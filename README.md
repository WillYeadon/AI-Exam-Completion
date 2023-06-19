## AI Exam Completion

# Overview

This repository contains scripts for extracting exam questions from '.tex' files and utilizing OpenAI's API for automatic completion. The process involves using a series of regular expressions to identify and extract the questions within the .tex files. These extracted questions are then sent to the API for a "cleaning" process, where modifications are made to ensure the extracted LaTeX code is compilable. Once the questions are cleaned, a second script sends them, along with system prompts, back to the API for generating answers.

In addition, there is a script dedicated to extracting marks associated with each question. Subsequently, the questions, answers, and marks are combined using a Jinja template to create completed exam PDFs for each year.

Read the full paper [here](https://arxiv.org).

# Installation

The repository contains all the scripts required to process a series of .tex files used for Physics exams and generate completed PDFs. However, please note that the API keys have been removed. To use the scripts, you will need to create an account on OpenAI and generate your own API keys. Additionally, since the exam questions cannot be publicly released, the "example-raw-tex" folder contains only blank "example questions" for demonstration purposes.

It is important to keep a close eye on what you're actually extracting from the .tex files thus I recommend running the scripts individually. In principle, you can loop through all the years to create a single large database. However, I found it more efficient to keep things segregated by year and use a different API key for each run of the response script, allowing for parallel processing of the years. 

Once you have downloaded the repository and added your API keys, start with "run-questions.py" to execute all the question extraction scripts. This should create a file 'questions-2020-checked.xlsx'. If you create another column along the lines of '=IF(G2="OKAY", F2, G2)' then paste the values of this column back into the cleaned questions column you should be left just the API-cleaned questions. Again, you can modify the script to automate this but I recommend looking at the questions yourself to ensure they're what you want. Close inspection of the example will reveal Q2a in the 'Introductory physics' file extracted both 2a and 2b so you'd need to manually delete 2b! I found a useful heurisitic for catching this was to measure the length of the question in another column and check the ones that are over say 2x or 3x the average.

After you're happy with the cleaned questions, run "run-mark-numbers.py" to add the corresponding marks to the questions along with ensuring the question numbers at apt. Following this, run 'exam-response-script.py' to get the AI to answer each question followed by 'latex-response-script.py' to check the latex and have the AI alter if (if needs be). You'll have to look at the cells where 'The latex is correct' is not present can copy them over to the 'responses column'.

Finally you're read to create the pdfs. Running 'output_answers.py' should do this for all of your exams.





