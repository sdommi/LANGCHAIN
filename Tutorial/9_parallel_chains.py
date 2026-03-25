import os
from dotenv import load_dotenv 
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableLambda,RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")

def demonstrate_str_parser(topic:dict):
    topic = topic.get("topic", "artificial intelligence")
###task1: create a prompt template for linkedin post generation
    prompt_template = ChatPromptTemplate.from_messages([
    ("system", "you are linkedin post generator"),
    ("human", "create a post for the following topic : {topic} ")
])

##task2 : Call the LLM with prompt template and get the response
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)


##task3: Create an instance of StrOutputParser
    str_parser = StrOutputParser()

##task3: Demonstrate StrOutputParser usage separately
# StrOutputParser extracts the string content from LLM responses
# It's useful when you want just the text output, not the full response object

# Create a simple chain: prompt -> llm -> string parser
    str_chain = prompt_template | llm | StrOutputParser()

# Invoke the chain with a topic
    str_result = str_chain.invoke({"topic": topic})

    print("Generated LinkedIn Post:")
    print(str_result)



if __name__ == "__main__":
    
    demonstrate_str_parser({"topic": "langchain"})