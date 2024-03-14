#write function that automates the call

import openai
from langchain.llms import OpenAI
from langchain.schema import BaseOutputParser
from langchain.chat_models import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import SinglePromptChain
from langchain.schema import BaseOutputParser
from configs import PublicationConfigs as publicationConfigs
from promptDict import promptDictGenerator

llm = OpenAI(open_api_key="...")
chat_model = ChatOpenAI()
    
class PublicationBot:
    """
    Fabricates data and a write-up of a randomized controlled trial.
    Args:
        fillerIntervention: intervention on which query is initially run
        finalIntervention: intervention on which query outputs data and results
        population: population on which intervention is run
        outcome: outcome impacted by intervention
        balanced covariates: features on which treatment is balanced
        sampleSize: sample size of test
    """
    def __init__(self, 
                 
                 fillerIntervention: str = 'VitaminSupplements',
                 finalIntervention: str = 'FirearmPossession', 
                 population: str = 'Students',
                 outcome: str = 'TestScores',
                 balancedCovariates: list = ['age', 'race', 'socioeconomic status'],
                 sampleSize: float = 1050
                 ):
        
        pconfigs = publicationConfigs()
        pdictgen = promptDictGenerator()
        self.fillerIntervention = fillerIntervention
        self.finalIntervention = finalIntervention
        self.population = population
        self.outcome = outcome
        self.balancedCovariates = balancedCovariates
        self.sampleSize = sampleSize
        self.rawPromptOutput = self.generatePromptOutput()
    
        def generatePromptOutput(self):
            promptDict = self.getPromptDict()
            output_dict = {}
            for promptType, prompt in promptDict.items():
                chat_prompt = ChatPromptTemplate.from_messages([
                                ("system", pconfigs.paperWriterSystem),
                                ("human", prompt),
                            ])
                chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()
                #somehow capture output withLangChain, let's call it output now as a filler
                output = chain.run()
                output_dict[promptType] = output
            return output_dict
    
        def generateRefinedPromptOutput(self, initialOutputDict: dict):
            
            refined_output = {}
            #generate critique (first on rawPromptOutput)
            self.rawPromptOutput 
            critique_dict = {}
            for promptType, response in initialOutputDict.items():
                chat_prompt = ChatPromptTemplate.from_messages([
                                ("system", pconfigs.paperEvaluatorSystem),
                                ("human", prompt),
                            ])
                chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()
                #somehow capture output withLangChain, let's call it output now as a filler
                output = chain.run()
                critque_dict[promptType] = output
                
                #save critique somewhere
            
            #generate revised output
            for promptType, prompt in promptDict.items():
                chat_prompt = ChatPromptTemplate.from_messages([
                                ("system", pconfigs.paperWriterSystem),
                                ("human", prompt),
                            ])
                
                #save new output somewhere
            
            #return new output


        def getPromptDict(self):
            promptDict = pdictgen.pd(population = self.population,
                                        outcome = self.outcome,
                                        sampleSize = self.sampleSize,
                                        fillerIntervention = self.fillerIntervention,
                                        finalIntervention = self.finalIntervention)
            return promptDict
           
        
        def generateDataset(self, ):
            #run 

        

    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        # print(completion.usage)
        return completion.choices[0].message.content


class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""


    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")
    



for prompt in prompts:
    # Set up the chain for processing
    chain = SinglePromptChain(llm=llm, prompt=prompt)
    
    # Process the prompt and get the output
    output = chain.run()
    
    # Save the output
    outputs.append(output)

# Now you can refer to the outputs later in the code
for i, output in enumerate(outputs):
    print(f"Output {i}: {output}")

# Example of referring to a specific output
# Let's say you want to refer to the second output
second_output = outputs[1]
print(f"The second output was: {second_output}")