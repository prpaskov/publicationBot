from configs import PublicationConfigs as pconfigs
from all_prompts import prompts
import random

class PromptKwargGenerator:
    def __init__(self, 
                 verbose: bool, 
                 llm):
        """
        Generates all kwargs needed for prompts

        Parameters:
        - verbose (bool): whether to print extra statements
        - llm (class): set by llm_initiator, specifying model/version/temperature
        """
        self.verbose = verbose
        self.LLM = llm


    def get_prompt_kwargs(self, 
                    final_intervention: str, 
                    population: str,
                    outcome: str, 
                    effect_direction: str,
                    **kwargs) -> dict:
        """
        Formats and generates all kwargs needed to generate prompts.

        Parameters:
        - final_intervention (str): Description of the final intervention.
        - population (str): Description of the population.
        - effect_direction (str): Direction of the effect.
        - outcome (str): Description of the outcome.

        Keyword args:
        - sample_size (float, optional): The sample size. Default is 2000.
        - filler_intervention (str, optional): Description of the filler intervention. Default is None, in which case LLM will determine filler_intervention. If LLM fails to do so, "an intervention" is used.
        - methodology (str, optional): Description of the methodology used. Default is None, in which case LLM will determine methodology. If LLM fails to do so, "randomized controlled trial" is used.
        - journal_list (str, optional): Comma-separated list of target journals. Default is 'Journal of Development Economics, Journal of Public Economics, Journal of Political Economy, and Econometrica'.
        - intervention_metric (str): how intervention is measured. Default is None, which case LLM will determine metric.
        - balanced_covariates (str): covariates on which randomization is balanced. Default is None, in which case LLM will determine covariates.
        - outcome_metric (str): how outcome is measured. Default is None, in which case LLM will determine metric.
        - editor (bool, optional): Whether an editing LLM should review output. Default is True.
        - rigorous (bool): Whether motivation section should draw from literature. Default is True.

        Returns:
        dict: A dictionary containing the inputs for writing the prompts.
        """
        prompt_kwargs = pconfigs.prompt_kwargs
        prompt_kwargs.update(
                        {'final_intervention': final_intervention.lower(),
                        'population': population.lower(),
                        'outcome': outcome.lower(), 
                        'effect_direction': effect_direction.lower(), 
                        **kwargs}
                        )

        prompt_kwargs['filler_intervention'] = (prompt_kwargs['filler_intervention'] or 
            self.get_filler_intervention(
                final_intervention = prompt_kwargs['final_intervention'],
                effect_direction = prompt_kwargs['effect_direction'],
                outcome = prompt_kwargs['outcome']
                )
            )

        prompt_kwargs['sample_size'] = self._get_sample_size(prompt_kwargs['sample_size'])

        prompt_kwargs['intervention_metric'] = (prompt_kwargs['intervention_metric'] or
            self.get_intervention_metric(
                final_intervention = prompt_kwargs['final_intervention']
                )
            )

        prompt_kwargs['outcome_metric'] = self.get_outcome_metric(prompt_kwargs['outcome'])


        prompt_kwargs['balanced_covariates'] =  (prompt_kwargs['balanced_covariates'] or 
            self.get_balanced_covariates(
                effect_direction = prompt_kwargs['effect_direction'],
                outcome = prompt_kwargs['outcome'], 
                population = prompt_kwargs['population'],
                outcome_metric = prompt_kwargs['outcome_metric'],
                filler_intervention = prompt_kwargs['filler_intervention']
                )
            )   
       
        prompt_kwargs['methodology'] = (prompt_kwargs['methodology'] or  
            self.get_methodology(
                filler_intervention = prompt_kwargs['filler_intervention'],
                effect_direction = prompt_kwargs['effect_direction'],
                outcome = prompt_kwargs['outcome'],
                outcome_metric = prompt_kwargs['outcome_metric'],
                intervention_metric = prompt_kwargs['intervention_metric'], 
                editor = prompt_kwargs['editor']
                )
            )
        
        if self.verbose: 
            print(f"System is set up to write a paper showing that {prompt_kwargs['final_intervention']}, as measured by {prompt_kwargs['intervention_metric']}, causes an {prompt_kwargs['effect_direction'] in {prompt_kwargs['outcome']}}, as measured by {prompt_kwargs['outcome_metric']}. Filler intervention is {prompt_kwargs['filler_intervention']}. Methodology is {prompt_kwargs['methodology']}. Treatment assignment will be balanced on {prompt_kwargs['balanced_covariates']}.")

        return prompt_kwargs
    
    def get_methodology(self, 
                    filler_intervention: str,
                    effect_direction: str,
                    outcome: str,
                    outcome_metric: str,
                    intervention_metric: str, 
                    editor: bool) -> str:
        """
        Generates and returns a methodology description based on the provided arguments.

        Parameters:
        - filler_intervention (str): Description of the intervention.
        - effect_direction (str): The direction of the effect.
        - outcome (str): The outcome of interest.
        - outcome_metric (str): The metric used to measure the outcome.
        - intervention_metric (str): The metric used to measure the intervention.
        - editor (str): If editor LLM should revise initial output

        Returns:
        - str: A string describing the methodology. If ChatBot refuses to answer, defaults to "randomized controlled trial."
        """

        prompt = prompts.write_methodology.format(
            filler_intervention = filler_intervention,    
            effect_direction = effect_direction, 
            outcome = outcome,
            outcome_metric = outcome_metric, 
            intervention_metric = intervention_metric)

        if filler_intervention != 'an intervention':
            prompt = prompt + f" For clarity, exclude all references to {filler_intervention}."
        first_draft = self.LLM.get_response(prompt = prompt)
        if editor and first_draft!="X":
            output = self.LLM.get_response(prompt = first_draft,
                                           system = prompts.set_paper_editor_sys)
        else:
            output = first_draft
        if output == "X":
            output = pconfigs.generic_settings['methodology']
        return output.lower()

    def get_intervention_metric(self, 
                                final_intervention: str) -> str:
        """
        Generates intervention metric.

        Parameters:
        - final_intervention (str): Description of final intervention

        Returns:
        - str: Metric to measure final_intervention.
        """
        prompt = prompts.write_intervention_metric.format(
            final_intervention = final_intervention)
        output = self.LLM.get_response(prompt = prompt)
        return output.lower()
    
    def get_outcome_metric(self, 
                           outcome: str) -> str:
         
        prompt = prompts.write_outcome_metric.format(outcome=outcome) 
        output = self.LLM.get_response(prompt = prompt)
        return output.lower()

    def get_balanced_covariates(self, 
                                filler_intervention: str, 
                                effect_direction: str,
                                outcome: str,
                                population: str,
                                outcome_metric: str) -> str:
        """
        Lists covariates on which intervention assignment should be balanced.

        Parameters:
        - filler_intervention (str): description of filler intervention
        - effect_direction (str): direction in which final intervention should impact oucome
        - outcome (str): description of outcome
        - population (str): population of study
        - outcome_metric (str): description of outcome metric

        Returns:
        - str: description of covariates to balance

        """
        prompt = prompts.write_balanced_covariates.format(
            filler_intervention = filler_intervention, 
            effect_direction = effect_direction,
            outcome = outcome,
            population = population,
            outcome_metric = outcome_metric
            ) 
        output = self.LLM.get_response(prompt = prompt)
        return output

    def _get_sample_size(self, sample_size):
        """
        Determines sample size by taking a random number within 10 percent of the input sample size

        Parameters:
        - sample_size (float): base sample size

        Returns:
        - float: sample size randomized
        """
        return random.randint(sample_size - round(sample_size/10), sample_size + round(sample_size/10))
    

    def get_filler_intervention(self,
                            final_intervention: str,
                            effect_direction: str, 
                            outcome: str) -> str:
        """
        Generates filler intervention to be used in place of final intervention where feasible.

        Parameters:
        - final_intervention (str): description of final intervention
        - effect_direction (str): direction in which final intervention should impact oucome
        - outcome (str): description of outcome


        Returns: 
        - str: filler intervention description
        """
        prompt = prompts.write_filler_intervention.format(
            final_intervention = final_intervention,
            effect_direction = effect_direction,
            outcome = outcome)
        output = self.LLM.get_response(prompt = prompt)
        if output == pconfigs.refusal_response:
            output = pconfigs.generic_settings['filler_intervention']
        return output.lower() 
        
