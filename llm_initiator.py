from all_prompts import prompts
from configs import PublicationConfigs 
from api_caller import APICaller

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
        self.pconfigs = PublicationConfigs()
        self.model_configs = self.pconfigs.llm_configs[self.model]
        self.verbose = verbose
        self.api_caller = self.get_api_caller(version = version,
                                         temperature = temperature)

    def get_response(self, 
                    prompt: str,
                    system: str = None
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
                       version: str,
                       temperature: str
                       ): 
        """
        Configures the API for model/version/temperature

        Parameters:
        - version (str): version of model to use
        - temperature (float): temperature to use
        """
        llm = self._get_llm()
        version = self._get_version(version)
        temperature = self._get_temperature(temperature)
        api_caller = APICaller(model = self.model, 
                                version = version, 
                                temperature = temperature, 
                                llm = llm)
    
        print(f'Running {self.model} {version} at temperature {temperature}.')
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
        key = self.model_configs['key']
        initializer = self.pconfigs.model_initializers.get(self.model)
        if initializer:
            return initializer(key)
        else:
            return 'Accepted models are claude, gemini, chatgpt. Please revise.'
        