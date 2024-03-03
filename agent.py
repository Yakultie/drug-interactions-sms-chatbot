from langchain.tools.base import StructuredTool
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

import mongodb
import drugapi
import twilioapi

chat = ChatOpenAI(model_name="gpt-4", temperature=0.0)

from typing import Optional

def get_user_past_messages(userId: Optional[str] = None) -> list:
    """Tool that retrieves a list of past messages sent by a user given the user's User ID."""
    return mongodb.retrieveUserMessagesBeforeCurrentSession(userId)

def get_drug_interactions(medicine_names: Optional[list] = None) -> list:
    """Tool that retrieves information about interactions between drugs given their medicine name and returns such interaction information in a list."""
    return drugapi.getDrugInteractions(medicine_names)

def get_adverse_reactions(medicine_name: Optional[str] = None) -> str:
    """Tool that retrieves notable adverse reactions for a specific medicine reported throughout the United States."""
    return drugapi.getAdverseReactions(medicine_name)

def get_sms_clarification(userId: Optional[str], question: Optional[str] = None) -> str:
    """Tool that asks the user a question via SMS for clarification and returns the user's response to that question."""
    return twilioapi.getClarification(userId, question)

def deliver_final_answer(userId: Optional[str], final_answer: Optional[str] = None) -> bool:
    """Tool that delivers the final answer to the user using their User ID. Returns True if delivered successfully, returns False if not delivered successfully."""
    return twilioapi.deliverFinalAnswer(userId, final_answer)

get_user_past_messages_tool = StructuredTool.from_function(get_user_past_messages)
get_drug_interactions_tool = StructuredTool.from_function(get_drug_interactions)
get_adverse_reactions_tool = StructuredTool.from_function(get_adverse_reactions)
get_sms_clarification_tool = StructuredTool.from_function(get_sms_clarification)
deliver_final_answer_tool = StructuredTool.from_function(deliver_final_answer)

tools = [get_user_past_messages_tool, get_drug_interactions_tool, get_adverse_reactions_tool, get_sms_clarification_tool, deliver_final_answer_tool]
agent_chain = initialize_agent(tools, 
                               chat, 
                               agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
                               verbose=True)

def entry_point(userId, query):
    prompt = """
    My user ID is '{0}'. Please consider my past messages, which may include other medicines I have taken recently and if so, ask me to clarify if I am still actively taking each of the medicines.
    Use the SMS clarification tool to ask me for clarifications. 
    Then, use the information to answer the following question: {1}
    Try different variations of the medicine name if the one provided by the user is invalid. If you are still unable to come to a valid medicine name, stop immediately and tell me in your response. 
    Deliver the final answer using the Deliver Final Answer tool. 
    Answer in a way that is easily understandable by a patient: """.format(userId, query)
    agent_chain(prompt)
