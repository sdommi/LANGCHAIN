"""
LangChain Messages: A Comprehensive Guide
==========================================

Messages are the core units of communication in LangChain. They represent structured 
conversations between different roles (system, user, assistant, etc.) and are used to 
interact with language models.

Key Message Types:
------------------

1. SystemMessage:
   - Sets the behavior and tone of the assistant
   - Example: "You are a helpful coding expert."
   - Usually the first message in a conversation

2. HumanMessage:
   - Represents user input or questions
   - What the user asks or tells the assistant
   - Example: "What is the capital of France?"

3. AIMessage:
   - Represents assistant responses
   - What the model generates
   - Example: "The capital of France is Paris."

4. FunctionMessage:
   - Used when calling external tools/functions
   - Returns the result of a tool call
   - Example: Result from a calculator or API

5. ToolMessage:
   - Similar to FunctionMessage but for tool calls
   - Used with agents that call tools

Why Messages Matter:
--------------------
- Structure conversations into ordered sequences
- Maintain context for multi-turn interactions
- Enable role-based prompting (system → human → AI)
- Work seamlessly with LangChain chains and agents
- Support streaming and async operations

Common Patterns:
----------------
- Single turn: [SystemMessage] + [HumanMessage]
- Multi-turn: [System] + [Human, AI, Human, AI, ...]
- Tool use: [System] + [Human] + [AI] + [ToolMessage] + [AI]
"""

#
from langchain.messages import SystemMessage,HumanMessage
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment variables

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")

    conversation_messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is the capital of France? and tell me a joke"),
    ]
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)
    response = llm.invoke(conversation_messages).content.strip()
    print("Response:")
    print(response)

if __name__ == "__main__":
    main()

