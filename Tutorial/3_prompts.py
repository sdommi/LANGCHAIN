"""
LangChain Prompts: A Comprehensive Guide
=========================================

Prompts are the instructions and context provided to language models to generate
responses. In LangChain, prompts are structured templates that can include variables,
formatting, and conditional logic to create dynamic, reusable text generation workflows.

Key Prompt Types:
-----------------

1. String Prompts:
   - Simple text strings with optional variable interpolation
   - Example: "Tell me about {topic}"
   - Best for basic, single-turn interactions

2. ChatPromptTemplate:
   - Structured prompts for conversational AI
   - Composed of multiple message templates (system, human, AI)
   - Example: System message + Human message with variables
   - Ideal for multi-turn conversations and role-based prompting

3. FewShotPromptTemplate:
   - Includes examples in the prompt to guide the model's responses
   - Helps with specific formatting or reasoning patterns
   - Example: Providing sample Q&A pairs before the actual question

4. PromptTemplate:
   - Template-based prompts with variable substitution
   - Supports formatting and validation
   - Example: "Write a {style} summary of {text}"

Why Prompts Matter:
-------------------
- Control model behavior and output quality
- Enable dynamic content generation with variables
- Maintain consistency across similar tasks
- Support complex workflows with chains and agents
- Allow for easy experimentation and iteration

Common Patterns:
----------------
- Basic templating: Replace {variables} with actual values
- Conditional prompts: Include logic based on input parameters
- Multi-part prompts: Combine system instructions with user queries
- Example-based learning: Use few-shot examples for better results
- Chain integration: Connect prompts in sequential workflows

Examples:
---------
"""

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")

# Example 1: Simple String Prompt with Template
def simple_prompt_example():
    # Make it dynamic by getting user input
    length = input("Enter the length (e.g., brief, detailed): ").strip()
    topic = input("Enter the topic: ").strip()
    
    template = "Write a {length} description of {topic}."
    prompt = PromptTemplate.from_template(template)
    formatted = prompt.format(length=length, topic=topic)
    print("Simple Prompt Example:")
    print(formatted)
    print(template)
    print()

    # Invoke the LLM with the formatted prompt
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
    response = llm.invoke(formatted)
    print("LLM Response:")
    print(response.content)
    print()

# Example 2: Chat Prompt Template
def chat_prompt_example():
    role = input("Enter the role for the assistant (e.g., helpful, expert): ").strip()
    concept = input("Enter the concept to explain: ").strip()
    
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a {role} assistant."),
        ("human", "Explain {concept} in simple terms.")
    ])
    formatted = chat_template.format_messages(role=role, concept=concept)
    print("Chat Prompt Example:")
    for msg in formatted:
        print(f"{msg.type}: {msg.content}")
    print()

    # Invoke the LLM with the formatted chat messages
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
    response = llm.invoke(formatted)
    print("LLM Response:")
    print(response.content)
    print()

# Example 3: Few-Shot Prompt Template
def few_shot_example():
    examples = [
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "What is 3 + 5?", "answer": "8"}
    ]
    example_prompt = PromptTemplate.from_template("Q: {question}\nA: {answer}")
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="Q: {input}\nA:",
        input_variables=["input"]
    )
    formatted = few_shot_prompt.format(input="What is 7 + 3?")
    print("Few-Shot Prompt Example:")
    print(formatted)
    print()

if __name__ == "__main__":
    simple_prompt_example()
    chat_prompt_example()
    few_shot_example()    