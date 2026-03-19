import os
from dotenv import load_dotenv

# Sample OpenAI call using the official OpenAI Python client.
# Install: pip install openai python-dotenv
# Put your key in a .env file: OPENAI_API_KEY="sk-..."

from openai import OpenAI

load_dotenv()  # loads .env into environment variables


def chartbot():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to .env or environment.")
    client = OpenAI(api_key=api_key)

    print("Welcome to ChartBot! Ask any question and get a short, engaging answer.")
    print("Type 'quit' or 'exit' to stop.")

    while True:
        user_question = input("You: ").strip()
        if not user_question:
            continue
        if user_question.lower() in {"quit", "exit", "bye"}:
            print("ChartBot: Bye! Come back soon.")
            break

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are ChartBot, a concise and lively question-answering assistant."},
                {"role": "user", "content": user_question},
            ],
            max_tokens=150,
            temperature=0.85,
        )

        answer = response.choices[0].message.content.strip()
        print(f"ChartBot: {answer}\n")


if __name__ == "__main__":
    chartbot()
