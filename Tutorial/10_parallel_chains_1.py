import os
from dotenv import load_dotenv 
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableLambda,RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
import os 

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")

####CHAIN WITH PARALLEL STEPS

# TASK -1 [Prompt]

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a movie summarizer"),
    ("human", "Please summarize the movie in brief : {input}")])
# TASK - 2 [LLM]

llm_openai = ChatOpenAI(model="gpt-5-mini",temperature=0)
# TASK - 3 [Str Parser]

str_parser = StrOutputParser()
# TASK - 4 [Custom Runnable]
from langchain_core.runnables import RunnableLambda

def dictionary_maker(text:str)-> dict:

    return {"text" : text}

dictionary_maker_runnable = RunnableLambda(dictionary_maker)


#############Parallel Chain 1#############################
# TASK - 1 [Prompt]

linkedin_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a LinkedIn post generator"),
    ("human", "Create a post for the following text for LinkedIn: {text}")])

# TASK - 2 [LLM]

llm_openai = ChatOpenAI(model="gpt-5-mini",temperature=0)

# TASK - 3 [Str Parser]

str_parser = StrOutputParser()

chain_linkedin = linkedin_prompt | llm_openai | str_parser


######################Parallel Chain 2#########################
from langchain_core.runnables import RunnableParallel, RunnableLambda
def insta_chain(text:dict):

    text = text["text"]

    # TASK - 1 [Prompt]
    insta_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Instagram post generator"),
    ("human", "Create a post for the following text for Instagram: {text}")])
    
    # TASK - 2 [LLM]
    llm_openai = ChatOpenAI(model="gpt-5-mini",temperature=0)

    # TASK - 3 [Str Parser]
    str_parser = StrOutputParser()

    chain_insta = insta_prompt | llm_openai | str_parser

    result = chain_insta.invoke(text)

    return result

insta_chain_runnable = RunnableLambda(insta_chain)

############Final Orchestration##########################
final_chain = ( 
                    prompt_template | 
                    llm_openai | 
                    str_parser | 
                    dictionary_maker_runnable |
                    RunnableParallel(branches = {"linkedin": chain_linkedin, "instagram": insta_chain_runnable})
)

final_chain.invoke("AVATAR")
################Chain as a Runnable#########
# TASK - 1 [Beautify Function]

def beautify(final_response:dict)-> dict:

    linkedin_response = final_response['branches']['linkedin']
    instagram_response = final_response['branches']['instagram']

    return {"linkedin": linkedin_response, "instagram": instagram_response}

beautify_runnable = RunnableLambda(beautify)


# TASK - 2 [Final Chain]

# final_chain 


# Beautified Chain
beautified_chain = final_chain | beautify_runnable

res=beautified_chain.invoke("Pushpa")
print(res)






