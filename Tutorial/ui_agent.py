import os
import sqlite3
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import base64

load_dotenv()
DB_PATH = os.path.join(os.path.dirname(__file__), "ui_agent.db")


def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, question TEXT, answer TEXT, created_at TEXT)")
    conn.commit()
    conn.close()


def record_answer(question, answer):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO notes (question, answer, created_at) VALUES (?, ?, datetime('now'))", (question, answer))
    conn.commit()
    conn.close()


def run_agent(question):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY is not set in .env"
    client = OpenAI(api_key=api_key)
    prompt = (
        "You are a friendly assistant. Answer the user question briefly and clearly.\n"
        f"Question: {question}\n"
    )
    resp = client.responses.create(model="gpt-4.1-mini", input=prompt)
    text = resp.output[0].content[0].text if resp.output else str(resp)
    return text


def main():
    st.title("Small UI Agent")
    st.write("Ask the agent anything and save Q/A notes.")

    ensure_db()
    question = st.text_input("Your question:")
    if st.button("Run Agent"):
        if not question:
            st.warning("Please enter a question.")
        else:
            answer = run_agent(question)
            st.markdown("**Answer:**")
            st.write(answer)
            record_answer(question, answer)

    st.write("---")
    st.write("### Past Q/A")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT question, answer, created_at FROM notes ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    for q, a, created in rows:
        st.markdown(f"**{created}**: {q}")
        st.write(a)


if __name__ == "__main__":
    main()
