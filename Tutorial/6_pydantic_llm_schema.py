from pydantic import BaseModel, Field

from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model   


import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")   


class Employee(BaseModel):
    name: str = Field(..., description="The name of the employee")   
    age: int = Field(..., description="The age of the employee")
    salary: float = Field(..., description="The salary of the employee") 

if __name__ == "__main__":

    # Initiate structured output from LLM
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
    structured_llm = llm.with_structured_output(Employee)

    prompt = "Generate information for a fictional employee. Provide name, age, and salary."

    response = structured_llm.invoke(prompt)
    print("Structured output from LLM:")
    print(response)
    print()
    print("As JSON:")
    print(response.model_dump_json(indent=2))   

