import os
import json


# from langchain_community import ChatOpenAI
from langchain_openai import ChatOpenAI

# from langchain.chains import conversation, ConversationChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import llm

from config import Config

llm = ChatOpenAI(temperature=0, model="gpt-4o",
                 openai_api_key=Config.openAiApiKey)

# Flexible Prompt for Extracting Essential Information
essential_info_prompt = PromptTemplate.from_template(
    """
    From the text below, extract any personally identifiable or contextually significant information that the user has provided. 
    Organize the information into categories, and if any specific type of information is not provided, you may skip it.
    
    Potential categories include (but are not limited to):
    - Personal Information (e.g., Full Name, Date of Birth, Place of Birth)
    - Contact Information (e.g., Email Address, Phone Number, Social Media Handles)
    - Location Information (e.g., Current City, Country, Home Address)
    - Professional Information (e.g., Occupation, Employer, Education, Degrees)
    - Family Information (e.g., Marital Status, Spouse, Children)
    - Interests and Hobbies
    - Any other relevant information that can be inferred from the text.

    Provide the information in a structured format.

    Text: {text}
    """
)

# Create the LangChain LLMChain for extracting essential information
# essential_info_chain = LLMChain(llm=llm, prompt=essential_info_prompt)

# essential_info_chain.run()


def essential_analyser(text):

    response = llm.invoke(essential_info_prompt.format(text=text))

    print(response.content)
