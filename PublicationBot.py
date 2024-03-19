import utils
from prompt_kwarg_generator import PromptKwargGenerator
import configs
from llm import LLM
import google.generativeai as genai
import datetime
import re
import os
import prompts

class pubBot:
    """
    Fabricates data and a write-up of a causal inference paper.

    Parameters:
    - model (str): LLM to use (currently works with gemini, claude or chatGPT)
    - temperature (float): temperature of LLM. if input is less (greater) than possible min (max) of an LLM, will default to that LLM's min(max).
    - version (str): version of model to use
    - verbose (bool): prints output iteratively if True

    """
    def __init__(self, 
            model: str = 'chatgpt',
            temperature: float = None,
            version: str = None, 
            verbose: bool = False):
        
        self.verbose = verbose
        self.model = model.lower()
        self.LLM = LLM(model = model,
                        temperature = temperature,
                        version = version,
                        verbose = verbose)
        
    def write_paper(self, 
            final_intervention: str, 
            population: str,
            outcome: str, 
            effect_direction: str,
            save_output: bool = False,
            **kwargs) -> dict:
        """
        Writes a paper with Title, Motivation, Methdology, and Conclusion sections, providing evidence that final_intervention cuases an effect_direction in outcome.

        Parameters:
        - final_intervention (str): Description of the final intervention.
        - population (str): Description of the population.
        - effect_direction (str): Direction of the effect.
        - outcome (str): Description of the outcome.
        - save_output (bool): Saves code and paper to paths specified in configs.output_paths

        Keyword args (optional):
        - sample_size (float): The sample size. Default is 2000.
        - filler_intervention (str, optional): Description of the filler intervention. Default is None, in which case LLM will determine filler_intervention. If LLM fails to do so, "an intervention" is used.
        - methodology (str): Description of the methodology used. Default is None, in which case LLM will determine methodology. If LLM fails to do so, "randomized controlled trial" is used.
        - intervention_metric (str): how intervention is measured. Default is None, in which case LLM will determine metric.
        - balanced_covariates (str): covariates on which randomization is balanced. Default is None, in which case LLM will determine covariates.
        - outcome_metric (str): how outcome is measured. Default is None, in which case LLM will determine the metric.
        - editor (bool, optional): Whether an editing LLM should review output. Default is True.
        - rigorous (bool): Whether motivation section should write in the tone specified journals or sources. Default is True.
        - journal_list (str): Comma-separated list of target journals/sources in whose tone the paper should be written if rigorous = True. Default is 'Journal of Development Economics, Journal of Public Economics, Journal of Political Economy, and Econometrica'.


        Returns:
        dict: A dictionary containing the outputs of a paper, including code to create data, Motivation section, Methodology section, Conclusion section, Title, full text, and formatted full text.
        """
        prompt_kwarg_generator = PromptKwargGenerator(verbose = self.verbose, 
                                                      llm = self.LLM)
        prompt_kwargs = prompt_kwarg_generator.get_prompt_kwargs(final_intervention = final_intervention, 
                                            population = population, 
                                            outcome = outcome, 
                                            effect_direction = effect_direction, 
                                            **kwargs)
        prompt_dict = utils.generate_prompt_dict(**prompt_kwargs)
        output_dict = self.run_prompts(prompt_dict = prompt_dict, 
                                      editor = prompt_kwargs['editor'],
                                      rigorous = prompt_kwargs['rigorous'])
        if save_output:
            self._save_output(output_dict = output_dict,
                              effect_direction = effect_direction,
                              final_intervention = final_intervention, 
                              outcome = outcome)
        return output_dict
       
    def build_section(self, 
                section: str,
                prompt: str, 
                editor: bool) -> str:
        """
        Writes and edits a section of the research paper.

        Parameters:
        - section (str): section title
        - prompt (str): prompt to write section
        - editor (bool): whether second LLM should edit first draft output

        Returns:
        - str: section text
        """
        first_draft = self.LLM.get_response(prompt = prompt)
        if editor and not utils.response_is_refusal(first_draft): #and (self.model!='claude' and section!='Title'):
            edited = self.edit_paper(prompt = first_draft) 
            output = edited if not utils.response_is_refusal(edited) else first_draft
        else:
            output = first_draft
        for w in configs.remove_words:
            output = output.replace(w, '')
        return output

    def run_prompts(self, 
                    prompt_dict: dict, 
                    editor: bool, 
                    rigorous: bool):
        """
        Runs prompts and returns dict with output text

        Parameters:
        - prompt_dict (dict): dict containing prompts to write paper
        - editor (bool): whether editor should revise output
        - rigorous (bool): whether motivation section is written in tone of journals

        Returns:
        - dict: output with LLM text response to prompts
        """
        section_dict = {}
        for section, prompt in prompt_dict.items():
            if section == "Motivation_rigorous" and not rigorous:
                continue
            if section == "Bibliography":
                if 'Motivation_rigorous' in section_dict and not utils.response_is_refusal(section_dict['Motivation_rigorous']):
                    prompt = prompt.format(motivation = section_dict['Motivation_rigorous'])
                else:
                    prompt = prompt.format(motivation = section_dict['Motivation'])
            section_dict[section] = self.build_section(
                                        section = section,
                                        prompt = prompt, 
                                        editor = editor)
        output_dict = self._join_sections(section_dict,
                                          rigorous = rigorous)
        return output_dict
    
    def edit_paper(self, 
                   prompt:str):
        """
        Runs first_draft output by editor "Sia" to increase quality.

        Parameters:
        - prompt (str): input text

        Returns:
        - str: input string edited by Sia
        """
        output = self.LLM.get_response(prompt, 
                                   system = prompts.set_paper_editor_sys.format(refusal_response = configs.refusal_response))
        return output

    def format_paper(self, 
                     paper_text: str):
        """
        Takes in string text and returns text formatted for LaTeX

        Parameters:
        - prompt (str): input text

        Returns:
        - str: input text formatted for LaTeX
        """
        prompt = prompts.format_paper.format(paper_text=paper_text)
        output = self.LLM.get_response(prompt = prompt)
        return output

    def _join_sections(self, 
                    section_dict:dict,
                    rigorous: bool) -> dict:
        """
        Concatenates sections from section_dict as specified in configs.paper_order. 

        Parameters: 
        - section_dict (dict): dict whose keys are section name and values are section text
        - rigorous (bool): whether to write rigorous motivation section using inspiration from literature

        Returns: 
        - dict: input dictionary with paper_text entry (concatenated sections) 
        """
        if rigorous and not utils.response_is_refusal(section_dict['Motivation_rigorous']):
            section_dict['Motivation'] = section_dict['Motivation_rigorous']
        paper_text = '*BREAK**BREAK*'.join(f'{s}*BREAK**BREAK*{section_dict[s]}' 
                                           for s in configs.paper_order 
                                           if not utils.response_is_refusal(section_dict[s]))
        paper_text = paper_text.replace('\n', ' ').replace("\'","'" ).replace('*BREAK*', ' \n').replace("Title \n", "")
        section_dict['paper_text'] = paper_text

        return section_dict

    def _save_output(self, 
                    output_dict: dict, 
                    effect_direction: str,
                    final_intervention: str,
                    outcome: str):
        """"
        Saves data code and paper text text to folders specified in configs.output_paths

        Parameters:
        - output_dict (dict): dictionary containing results of paper writing prompts. must contains keys of 'Data Collection', 'Title', 'paper_text', and 'paper_text_formatted'
        - effect_direction (str): effect driection
        - final_intervention (str): Description of the final intervention.
        - outcome (str): Description of the outcome.

        Returns:
        - csv files saved to disk
        """
        current_date = datetime.date.today()
        file_name = (str(current_date).replace('-', '') 
                    + '_'
                    + self.LLM.model 
                    + '_'
                    + self.LLM.version 
                    + '_' 
                    + final_intervention.replace(' ', '_')
                    + f'_{effect_direction}_' 
                    + outcome.replace(' ', '_')
        )
        
        for section, sectionDict in configs.output_paths.items():
            output_content = output_dict[section]
            if output_content == 'X':
                print(f'{section} not generated by pubBot due to refusal: not saving to file.')
            else:
                os.makedirs(sectionDict['folder'], exist_ok=True)
                full_path = os.path.join(sectionDict['folder'], file_name + sectionDict['ending'])
                with open(full_path, 'w') as file:
                    file.write(output_content)
                    