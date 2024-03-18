import google.generativeai as genai
import configs

class LLMAPICaller:

    def __init__(self,
                model: str,
                version: str, 
                temperature: float,
                llm
                ) -> str:
        """ 
        Parameters:
        - model (str): model to use
        - version (str): model version to use
        - temperature (float): temperature of model to use
        - llm (instance): configured LLM for model/version using API key
        """
        self.model = model
        self.version = version 
        self.temperature = temperature
        self.llm = llm
    
    def call_api(self, 
                 prompt: str,
                 system: (str)
                 ):
        """
        Returns chat response from LLM

        Parameters:
        - prompt (str): prompt
        - system (str): system description. currently combined with prompt.

        Returns: 
        - str: LLM response
        """
        kwargs = {'prompt': prompt, 'system': system}
        if self.model.lower() == 'gemini':
            return self._get_gemini_response(**kwargs)
        elif self.model.lower() == 'chatgpt':
            return self._get_chatgpt_response(**kwargs)
        elif self.model.lower() == 'claude':
            return self._get_claude_response(**kwargs)
        else:
            return f'{model.lower()} not supported. Supported models are gemini, chatgpt, and claude.'

    def _get_gemini_response(self,
                            prompt: str,
                            system: str = None,
                            ) -> str:
        """ 
        Returns chat response from Gemini

        Parameters:
        - prompt (str): prompt
        - system (str): system description. currently combined with prompt.
        Returns:
        - str: Gemini text response 
        """
        prompt = f'{system} {prompt}'
        chat = self.llm.generate_content(
                                        prompt,
                                        generation_config=genai.types.GenerationConfig(
                                        candidate_count=1,
                                        temperature=self.temperature
                                        )
                                        )
        return chat.text
    
    def _get_claude_response(self,
                            prompt: str,
                            system: str = None,
                            ) -> str:
        """ 
        Returns chat response from Claude

        Parameters:
        - prompt (str): prompt
        - system (str): system description. currently combined with prompt.

        Returns:
        - str: Claude text response
        """
        chat = self.llm.messages.create(
                                        max_tokens=3024,
                                        system = system,
                                        messages=[
                                                {"role": "user", 
                                                "content": prompt}
                                                ],
                                        model = self.version,
                                        temperature = self.temperature
                                        )
        return chat.content[0].text

    def _get_chatgpt_response(self,
                            prompt: str,
                            system: str = None,
                            ) -> str:
        """ 
        Returns chat response from ChatGPT

        Parameters:
        - prompt (str): prompt
        - system (str): system description. currently combined with prompt.

        Returns:
        - str: ChatGPT text response
        """
        chat = self.llm.chat.completions.create(
                                                messages = [
                                                            {"role": "system", "content": system},
                                                            {"role": "user", "content": prompt}
                                                            ],
                                                model = self.version,
                                                temperature = self.temperature
                                                )
        return chat.choices[0].message.content
    
    
