"""
TypedDict for LLM Structured Output in LangChain
===============================================

TypedDict is a typing construct that allows you to define the structure of dictionaries
with type annotations. In LangChain, TypedDict can be used as an alternative to Pydantic
BaseModel for structured output parsing from language models.

Key Features:
-------------

1. TypedDict Definition:
   - Use class syntax to define dictionary keys and their types
   - Example: class Person(TypedDict): name: str; age: int

2. Structured Output:
   - LangChain's `with_structured_output()` method supports TypedDict
   - LLM responses are parsed into typed dictionary objects
   - Provides type safety and validation

3. Advantages over Pydantic:
   - Lighter weight (no runtime validation overhead)
   - More flexible for simple structures
   - Better performance for high-throughput applications

4. Usage in LangChain:
   - Define your TypedDict schema
   - Call llm.with_structured_output(YourTypedDict)
   - Invoke with a prompt that guides the LLM to output structured data

Example Use Cases:
------------------
- Simple data extraction from text
- API response parsing
- Form data validation
- Configuration objects
"""

from typing import TypedDict
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")

class EmployeeTypedDict(TypedDict):
    name: str
    age: int
    salary: float

if __name__ == "__main__":
    # Example of manual TypedDict usage
    emp_dict = {"name": "Alice", "age": 32, "salary": 65000.0}
    # Type checking would catch errors here if types don't match
    typed_emp: EmployeeTypedDict = emp_dict
    print("Manual TypedDict instance:")
    print(typed_emp)
    print()

    # Structured output from LLM using TypedDict
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
    structured_llm = llm.with_structured_output(EmployeeTypedDict)

    prompt = "Create a profile for a software engineer employee. Include name, age, and salary."

    response = structured_llm.invoke(prompt)
    print("Structured output from LLM (TypedDict):")
    print(response)
    print()
    print("Type of response:", type(response))
    print("Keys:", list(response.keys()) if isinstance(response, dict) else "Not a dict")