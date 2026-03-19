import os
import sqlite3
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(__file__), "agentic.db")


def setup_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER, total REAL, order_date TEXT)")
    c.execute("DELETE FROM products")
    c.execute("DELETE FROM orders")
    c.executemany(
        "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
        [
            ("Widget A", "hardware", 19.99),
            ("Widget B", "hardware", 29.99),
            ("Pro Plan", "software", 99.0),
            ("Support Add-on", "service", 49.0),
        ],
    )
    c.executemany(
        "INSERT INTO orders (product_id, quantity, total, order_date) VALUES (?, ?, ?, ?)",
        [
            (1, 2, 39.98, "2026-03-01"),
            (2, 1, 29.99, "2026-03-02"),
            (3, 4, 396.0, "2026-03-03"),
            (1, 5, 99.95, "2026-03-05"),
            (4, 2, 98.0, "2026-03-06"),
        ],
    )
    conn.commit()
    conn.close()


def run_sql_query(sql: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(sql)
        if sql.strip().lower().startswith("select"):
            rows = c.fetchall()
            columns = [d[0] for d in c.description] if c.description else []
            conn.close()
            return (columns, rows)
        else:
            conn.commit()
            conn.close()
            return ([], [["OK"]])
    except Exception as e:
        conn.close()
        raise


def sql_agent_loop():
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.2)

    print("=== SQL Agentic Bot ===")
    print("I can answer questions by generating SQL and running it on a local SQLite DB.")
    print("Type 'exit' to quit.")

    while True:
        question = input("User: ").strip()
        if question.lower() in {"exit", "quit", "bye"}:
            print("Bye!")
            break

        prompt = (
            "You are an SQL agent. The DB has tables: products(id, name, category, price) and orders(id, product_id, quantity, total, order_date).\n"
            "Generate only a single SQL SELECT statement to answer the question, with no explanatory text.\n"
            f"Question: {question}\n"
            "SQL:"
        )

        response = llm.invoke(prompt)
        raw_sql = getattr(response, "text", None) or getattr(response, "response", None) or str(response)
        print(f"Raw model output: {raw_sql}")

        # Extract SQL from output by searching for SELECT... (or WITH...)
        import re
        match = re.search(r"(select|with)[\s\S]*?;", raw_sql, flags=re.IGNORECASE)
        if match:
            sql = match.group(0).strip()
        else:
            # fallback: remove fences and use plain text
            cleaned = raw_sql.replace('```', '').strip()
            if cleaned.lower().startswith('sql:'):
                cleaned = cleaned.split(':', 1)[1]
            sql = cleaned.strip().rstrip(';') + ';'

        # Validate SQL begins with select or with
        if not sql.lower().lstrip().startswith(('select', 'with')):
            print(f"Could not parse a valid SELECT SQL from model output. Output was: {raw_sql}")
            print("Please ask a simpler question or provide explicit SQL.")
            continue

        print(f"Generated SQL: {sql}")

        try:
            columns, rows = run_sql_query(sql)
            if not rows:
                print("No rows returned.")
            else:
                print("Result:")
                print(" | ".join(columns))
                for r in rows:
                    print(" | ".join(str(x) for x in r))

                summary_prompt = (
                    "You are an assistant that summarizes SQL results.\n"
                    f"Question: {question}\n"
                    f"SQL: {sql}\n"
                    f"Columns: {columns}\n"
                    f"Rows: {rows}\n"
                    "Give a short analysis in one paragraph."
                )
                summary = llm.invoke(summary_prompt)
                summary_text = getattr(summary, "text", None) or getattr(summary, "response", None) or str(summary)
                print("Summary:")
                print(summary_text.strip())

        except Exception as e:
            print(f"SQL execution failed: {e}")
            print("Try a more basic question or ask for a simple query.")


if __name__ == "__main__":
    setup_db()
    sql_agent_loop()
