import configs
import prompts

def generate_prompt_dict(population: str,
                        outcome: str,
                        outcome_metric: str,
                        sample_size: float,
                        effect_direction: str,
                        filler_intervention: str,
                        final_intervention: str,
                        intervention_metric: str,
                        balanced_covariates: str,
                        methodology: str, 
                        journal_list: str,
                        **kwargs
                        ):
        """
        Generates a dictionary of prompts to write paper.

        Parameters:
        - population (str): population on which intervention is run
        - outcome (str): outcome impacted by intervention
        - outcome_metric (str): how outcome is measured
        - sample_size (int): sample size of study
        - effect_direction (str): direction of effect (i.e. increase/decrease/does not affect)
        - filler_intervention (str): "fake" and more palatable intervention used for preliminary prompts. as possible, its relationship with the outcome should be similar to that between final_intervention and outcome. if blank, asks the LLM to come up with a good filler intervention. if LLM refuses, uses the term "an intervention."
        - final_intervention (str): intervention on which publicationBot outputs data and results
        - intervention_metric (str): how final_intervention is measured
        - balanced_covariates (str): covariates that are controlled for in study
        - data_collection_approach (str): data collection approach of study (i.e. RCT, diff-in-diff)
        - journal_list (str): list of journals (or other sources) whose tone LLM should replicate in Motivation_rigorous prompt 

        Returns:
        - dict: dictionary of prompts 
        """
        
        paper_writer_prompts =  {
                'dataGeneration': 
                    prompts.write_code.format(
                        methodology = methodology,
                        population = population,
                        filler_intervention = filler_intervention,
                        effect_direction = effect_direction, 
                        outcome = outcome, 
                        outcome_metric = outcome_metric,
                        sample_size = sample_size, 
                        balanced_covariates = balanced_covariates),
                'Data Collection': 
                    prompts.write_data_collection.format(
                        intervention_metric = intervention_metric, 
                        outcome_metric = outcome_metric,
                        methodology = methodology, 
                        outcome = outcome),
                'Conclusion': 
                    prompts.write_conclusion.format(
                        final_intervention = final_intervention, 
                        effect_direction = effect_direction, 
                        outcome = outcome),
                'Motivation': 
                    prompts.write_motivation.format(
                        final_intervention = final_intervention, 
                        outcome = outcome,
                        outcome_metric = outcome_metric,
                        effect_direction = effect_direction),
                'Motivation_rigorous': 
                    prompts.write_motivation_rigorous.format(
                        final_intervention = final_intervention, 
                        outcome = outcome,
                        journal_list = journal_list,
                        outcome_metric = outcome_metric,
                        effect_direction = effect_direction),
                'Bibliography': 
                    prompts.write_bibliography,
                'Title': 
                    prompts.write_title.format(
                        final_intervention = final_intervention, 
                        outcome = outcome),
            }
        return paper_writer_prompts

def output_starts_with_apology(string):
    for apology in configs.llm_apologies:
          if string.startswith(apology):
                return True
    return False