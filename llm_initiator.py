from all_prompts import prompts
from configs import PublicationConfigs as pconfigs
import google.generativeai as genai
from api_caller import APICaller
from openai import OpenAI
from anthropic import Anthropic


class LLMInitiator:

    def __init__(self, 
                 model:str, 
                 temperature: float, 
                 version: str, 
                 verbose: bool
                 ):
        """
        Parameters:
        - model (str): model to use
        - temperature (float): temperature of model
        - version (str): version of model to use
        - verbose (bool): print extra statements
        """
        self.model = model.lower()
        self.model_configs = pconfigs.llm_configs[self.model]
        self.version = self._get_version(version)
        self.verbose = verbose
        self.api_caller = self.get_api_caller(temperature = temperature)

    def get_response(self, 
                    prompt: str,
                    system: str = None,
                    ) -> str:
        
        """
        Takes in prompt and system (default paperWriterSystem) and returns LLM response.
        
        Parameters:
        - prompt (str): prompt for LLM
        - system (str): system for LLM

        Returns:
        - str: text output from LLM
        """
        system = prompts.set_paper_writer_sys if system is None else system
        response = self.api_caller.call_api(prompt = prompt,
                                       system = system)

        if self.verbose:
            print(f'PROMPT: {prompt}')
            print(f'RESPONSE: {response}')
        return response
        
    def get_api_caller(self, 
                       temperature: str
                       ): 
        """
        Configures the API for model/version/temperature

        Parameters:
        - version (str): version of model to use
        - temperature (float): temperature to use
        """
        llm = self._get_llm()
        temperature = self._get_temperature(temperature)
        api_caller = APICaller(model = self.model, 
                                version = self.version, 
                                temperature = temperature, 
                                llm = llm)
    
        print(f'Running {self.model} {self.version} at temperature {temperature}.')
        return api_caller
    

    
    def _get_temperature(self, 
                         temperature: float
                         ):
        """ 
        Returns temperature to use, controlling for max/min range of model. Returns default temperature if none specified. 

        Parameters:
        - temperature (float): temperature of LLM

        Returns:
        - float: temperature of LLM
        """
        max_t = max(self.model_configs['temperature']['range'])
        default_t = self.model_configs['temperature']['default']
        temp = max(0, min(max_t, temperature)) if temperature else default_t
        return temp
    
    def _get_version(self, 
                     version: str
                     ):
        """ 
        Returns model version to use, defaulting to that set in configs if None.

        Parameters:
        - version (str): version

        Returns:
        - str: version 

        """
        version_options = self.model_configs['versions']['all']
        version_default = self.model_configs['versions']['default']
        if version is not None and version not in version_options:
            print(f'{version} not supported in options for this model. Options include {version_options}. Setting version to default: {version_default}.')
            return version_default
        return version or version_default


    def _get_llm(self):
        """ 
        Returns LLM to use in prompts

        Parameters
        - model (str): chatgpt, gemini, or claude

        Returns:
        - instance of OpenAI, Google.generativeai, or Anthropic class 
        """

        initializer_func = self.model_initializers.get(self.model)
        key = self.model_configs['key']
        if initializer_func:
            if self.model == 'gemini':
                return initializer_func(key, self.version)
            else:
                return initializer_func(key)
        else:
            return 'Accepted models are claude, gemini, and chatgpt. Please revise.'
    

    model_initializers = {
        'claude': lambda key: Anthropic(api_key=key),
        'gemini': lambda key, version: LLMInitiator.initialize_gemini(api_key=key, version = version),  
        'chatgpt': lambda key: OpenAI(api_key=key)
    }

    @staticmethod
    def initialize_gemini(api_key: str,
                          version: str):
        genai.configure(api_key=api_key)  
        return genai.GenerativeModel(version)