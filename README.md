## Overview
This is a collection of code I've used to create various AI benchmarking tests. In general there are two parts, an API script to generate AI answers to various questions students are assigned during physics modules and utility code to turn those answers into PDFs that can be marked, ideally blinded. 

The API used is from OpenAI but it shouldn't be too much fuss to change this code to work with other foundation models like Claude. The key challenge is converting learning/assessment materials into the "language" foundation models are comfortable in: 

* For written essays the process is trivial as text is essentially native to LLMs.
* For physics exams the main issue is parsing the latex equations. The solution I used was to compile the API responses in latex then send back the response and any error should it fail to compile. Be warned, error messages can be long so you'll be spending a lot on API calls!
* For coding assignments, I converted the raw .ipynb to .py files and ran the returned API calls into python. GPT-3.5 and GPT-4 are suprisingly good at returning error-free python if you're careful with the prompt engineering.

There are lots of methodological details in these preprints looking at: physics [essays](https://arxiv.org/abs/2403.05458), physics [written exams](https://arxiv.org/abs/2306.15609) and physics [coding assignments](https://arxiv.org/abs/2403.16977). 

The same code was used to look at Old English Essays [here](https://doi.org/10.21203/rs.3.rs-3483059/v1) If you're interested at doing this at your own institution please feel free to contact me for more details.

## Coding

The coding folder features the API input for the various assignments. It is a relatively straightforward process whereby the assignments are sent to the API and then the reponse is run as Python code with the plots extracted and saved. For obvious reasons actual student work can't be shared and unfortunately neither can the mark scheme / solutions be shared externally. However, I have included an `coding-generation/all-ai-images' folder which shows the plots generated by the various AI models in the [paper](https://arxiv.org/abs/2403.16977).