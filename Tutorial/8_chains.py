"""
Module: LangChain Chains Documentation

Chains in LangChain:
    Chains are a fundamental concept in LangChain that enable the composition 
    and sequencing of multiple language model calls and other components into 
    a single, cohesive workflow. They allow you to build complex applications 
    by linking together multiple steps where the output of one step becomes 
    the input of the next.

Why Use Chains:
    1. **Composition**: Combine multiple LLM calls and other tools into a 
       single, reusable pipeline.
    2. **State Management**: Automatically manage intermediate results and 
       pass data between steps.
    3. **Error Handling**: Handle failures gracefully with built-in retry 
       logic and error management.
    4. **Maintainability**: Simplify complex logic by breaking it into 
       discrete, manageable steps.
    5. **Reusability**: Create chains once and use them across different 
       parts of your application.
    6. **Monitoring**: Track and log the execution of each step for debugging 
       and optimization.

Example Without Chains (Manual Implementation):
    Without chains, you would manually manage the flow:
    - Call LLM 1, store result
    - Extract data from result
    - Pass to LLM 2, store result
    - Extract data again
    - Pass to LLM 3, etc.
    This becomes tedious, error-prone, and difficult to maintain.

Example With Chains (Structured Approach):
    With chains, you define the workflow once:
    - Create individual chain steps
    - Link them together using pipe operators or sequential composition
    - Execute the entire chain with a single call
    - Get the final result directly
    The chain handles all intermediate steps, data passing, and error handling 
    automatically, making your code cleaner and more maintainable.
"""

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")

# ============================================
# Example 1: Manual Step-by-Step Approach
# ============================================
def manual_step_by_step():
    print("=" * 60)
    print("EXAMPLE 1: Manual Step-by-Step Approach")
    print("=" * 60)
    
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
    
    # Step 1: Generate a topic
    topic_prompt = "Generate a creative topic for a blog post. Just one word or short phrase."
    topic_response = llm.invoke(topic_prompt)
    topic = topic_response.content
    print(f"Step 1 - Generated Topic: {topic}")
    print()
    
    # Step 2: Create an outline based on the topic
    outline_prompt = f"Create a 3-point outline for a blog post about: {topic}"
    outline_response = llm.invoke(outline_prompt)
    outline = outline_response.content
    print(f"Step 2 - Generated Outline:\n{outline}")
    print()
    
    # Step 3: Write an introduction based on the outline
    intro_prompt = f"Write a compelling introduction (3 sentences) for a blog post with this outline:\n{outline}"
    intro_response = llm.invoke(intro_prompt)
    introduction = intro_response.content
    print(f"Step 3 - Generated Introduction:\n{introduction}")
    print()

# ============================================
# Example 2: Using LangChain Chains with Pipe
# ============================================
def chain_with_pipe():
    print("=" * 60)
    print("EXAMPLE 2: Using LangChain Chains with Pipe Operator")
    print("=" * 60)
    
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
    
    # Step 1: Topic generation prompt
    topic_template = "Generate a creative topic for a blog post about {subject}. Just one word or short phrase."
    topic_prompt = PromptTemplate.from_template(topic_template)
    
    # Step 2: Outline generation prompt (takes topic as input)
    outline_template = "Create a 3-point outline for a blog post about: {topic}"
    outline_prompt = PromptTemplate.from_template(outline_template)
    
    # Build chain using pipe operator
    # topic_prompt -> llm -> extract content -> outline_prompt -> llm
    chain = (
        topic_prompt 
        | llm 
        | RunnableLambda(lambda x: x.content)  # Extract content from response
        | RunnableLambda(lambda x: {"topic": x})  # Format for next prompt
        | outline_prompt
        | llm
        | RunnableLambda(lambda x: x.content)
    )
    
    # Execute the chain
    result = chain.invoke({"subject": "artificial intelligence"})
    print("Chain Output (AI & Outline):")
    print(result)
    print()

# ============================================
# Example 3: Sequential Chain with Multiple Steps
# ============================================
def sequential_chain_steps():
    print("=" * 60)
    print("EXAMPLE 3: Sequential Chain with Multiple Manual Steps")
    print("=" * 60)
    
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
    
    # Step 1: Analyze user input
    step1_template = "Analyze this query and identify the main topic: {query}"
    step1_prompt = PromptTemplate.from_template(step1_template)
    
    # Step 2: Generate answer
    step2_template = "Answer this question comprehensively: {question}"
    step2_prompt = PromptTemplate.from_template(step2_template)
    
    # Step 3: Summarize
    step3_template = "Summarize this answer in 2 sentences:\n{answer}"
    step3_prompt = PromptTemplate.from_template(step3_template)
    
    # Create a multi-step chain
    def extract_content(response):
        return response.content
    
    chain = (
        step1_prompt
        | llm
        | RunnableLambda(extract_content)
        | RunnableLambda(lambda x: {"question": x})
        | step2_prompt
        | llm
        | RunnableLambda(extract_content)
        | RunnableLambda(lambda x: {"answer": x})
        | step3_prompt
        | llm
        | RunnableLambda(extract_content)
    )
    
    # Execute with a user query
    query = "How does machine learning work?"
    result = chain.invoke({"query": query})
    print(f"User Query: {query}")
    print(f"Final Summary:\n{result}")
    print()

if __name__ == "__main__":
    manual_step_by_step()
    chain_with_pipe()
    sequential_chain_steps()