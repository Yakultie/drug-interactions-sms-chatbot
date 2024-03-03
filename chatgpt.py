from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain import LLMChain

def gpt3(template, input_variables, variable_dictionary):
    llm = ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo-0613")
    
    prompt = PromptTemplate(template=template, input_variables=input_variables)

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    response = llm_chain.run(**variable_dictionary)
    
    return response

def gpt4(template, input_variables, variable_dictionary):
    llm = ChatOpenAI(temperature=0.9, model_name="gpt-4-0613")
    
    prompt = PromptTemplate(template=template, input_variables=input_variables)

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    response = llm_chain.run(**variable_dictionary)
    
    return response
