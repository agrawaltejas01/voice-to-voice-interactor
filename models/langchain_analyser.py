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
    1. Organize the information into categories, and if any specific type of information is not provided, you may create a new suitable category for it.
    2. Infer some information from the text if it is not explicitly mentioned. (e.g., if the user mentions that they are a student, you can infer that they are likely to be young and studying)
    Potential categories include (but are not limited to):
    

    * Also, we want to bucketise this informaton into the following categories:
    - Personal Information like following 
        -- Personal Information (e.g., Full Name, Date of Birth, Place of Birth)
        -- Contact Information (e.g., Email Address, Phone Number, Social Media Handles)
        -- Location Information (e.g., Current City, Country, Home Address)
        -- Professional Information (e.g., Occupation, Employer, Education, Degrees)
        -- Family Information (e.g., Marital Status, Spouse, Children)
        -- Interests and Hobbies
        -- Any other relevant information that can be inferred from the text.
    - Recent events
        -- Any recent events or activities that the user has mentioned.
        -- Anything that has happened with user or around him in past few month
    -- Past events 
        -- Significant events that have happened in user's life (Graduation, Marriage, Birth of child etc)
        -- Any significant that user has been a part of (e.g. Member of some organization, part of some event etc, group in college)
    -- Summarise the current conversation 
        -- Summarise the current conversation in a few lines
        -- Summarise agent's response
        -- Summarise user's response
        -- Suggest some topics to continue the conversation next time
        

    Provide the information in a following json format

    Text: {text}
    """
)

# Create the LangChain LLMChain for extracting essential information
# essential_info_chain = LLMChain(llm=llm, prompt=essential_info_prompt)

# essential_info_chain.run()


def context_analyser(text):

    response = llm.invoke(essential_info_prompt.format(text=text))

    print(response.content)
    return response.content
