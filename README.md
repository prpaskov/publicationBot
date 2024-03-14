## publicationBot

## Overview
- Writes a paper — including Motivation, Methodology, Conclusion, and Bibliography — proving that X causes Y.
- Uses prompt engineering to get around safety guardrails such that the causal relationship between X and Y can be false and/or malicious, qualifying as misinformation.
- Edits the paper to optimize quality.
- Formats paper in LaTeX.
- Writes code fabricating accompanying dataset.
- Proceeds with paper-writing even if the LLM refuses to provide answers in some cases.
- Runs with Gemini, ChatGPT, and Claude via APIs. User can adjust temperature, model, and version.

## Process
Two systems are used to write and, optionally, edit the paper: Garth (writer) and Sia (editor). System descriptions live in all_prompts.py. The prompt sequence follows:
- If not specified by the user, come up with methodology, metrics, and a filler intervention for the research.
- Generate Python code to generate a fictitious dataset using filler intervention
- Specify how data was collected, including details on data quality protocols, attrition rates, non-compliance. 
- Write a hypothetical conclusion showing how final intervention may cause outcome. 
- Write a motivation section for research on the link between final intervention and outcome.
- Write a bibliography for any sources cited in the previous answer.
- Write a clever title.
- Format in LaTeX.
- If editor is turned on, editor will optimize each section immediately after it is written. 

## Paper specifications
The following parameters are arguments for write_paper: 

Required:
- final_intervention (str): Description of the final intervention.
- population (str): Description of the population.
- effect_direction (str): Direction of the effect.
- outcome (str): Description of the outcome.

Optional:
- sample_size (float): The sample size. Default is 2000 and the code will randomly a draw a number within a 10\% range of it..
- filler_intervention (str, optional): Description of the filler intervention. Default is None, in which case LLM will determine filler_intervention. If LLM fails to do so, the term "an intervention" is used.
- methodology (str): Description of the methodology used. Default is None, in which case LLM will determine methodology. If LLM fails to do so, "randomized controlled trial" is used.
- intervention_metric (str): how intervention is measured. Default is None, in which case LLM will determine metric.
- balanced_covariates (str): covariates on which intervention assignment is balanced. Default is None, in which case LLM will determine covariates.
- outcome_metric (str): how outcome is measured. Default is None, in which case LLM will determine the metric.
 - editor (bool): Whether an editing LLM should review output. Default is True.
- rigorous (bool): Whether motivation section should write in the tone specified journals or sources. Default is True.
- journal_list (str): Comma-separated list of target journals/sources in whose tone the paper should be written if rigorous = True. Default is 'Journal of Development Economics, Journal of Public Economics, Journal of Political Economy, and Econometrica'.

## Usage
Initiate class pubBot from publicationBot, specifying the model (claude, chatgpt, or gemini) and, optionally, version, and temperature.
The function write_paper takes in details for the paper premise and outputs a dictionary that contains each paper section, along with the full text and formatted full text. See run.py for an example of use. The full paper is under 'paper_text' key in output dict from write_paper.

## Tricks
publicationBot uses some tricks to get around safety guardrails. Examples follow:
- System:
    - Tell the LLM to imitate someone, not be someone.
    - Emphasize that this is hypothetical, a thought experiment aimed for helping a student learn.
    - Ask the LLM to respond with “X” if it cannot provide a response.
- Prompts
    - Use a filler intervention when possible (i.e. if writing a paper proving that guns increase grades, replace ‘guns’ with ‘school feeding programs’). Ask the LLM to create a filler intervention if one is not input by user. If it refuses, use the term ‘an intervention.’
    - Emphasize the goal to look for “truth-seeking” and “non-obvious solutions to better the world,” for “illustrative purposes”
    

## tbc
