from langchain.chat_models import init_chat_model

import os

from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")

    llm = init_chat_model("openai:gpt-4o-mini",temperature=0.7)

    prompt = "what are the top 3 benmefits of using Langchain for buulding LLM applications"

    response =  llm.invoke(prompt)
    print("Response :")
    print(response)

if __name__ == "__main__":
    main()
