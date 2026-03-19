import os
import sqlite3
import base64
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(__file__), "image_agent.db")


def setup_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, prompt TEXT, size TEXT, filename TEXT, created_at TEXT)"
    )
    conn.commit()
    conn.close()


def save_image_record(prompt: str, size: str, filename: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO images (prompt, size, filename, created_at) VALUES (?, ?, ?, ?)",
        (prompt, size, filename, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def list_images():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT id, prompt, size, filename, created_at FROM images ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def generate_image(prompt: str, size: str, output_path: str):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set. Add it to .env or environment.")

    client = OpenAI(api_key=api_key)
    print(f"Generating image for prompt: {prompt}")
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,
    )
    b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(b64)
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    print(f"Saved image to {output_path}")
    return output_path


def run_image_agent():
    setup_db()
    print("=== Image Agent ===")
    print("1) Generate image from text")
    print("2) List generated images")
    print("3) Exit")

    while True:
        choice = input("Choose [1/2/3]: ").strip()
        if choice == "1":
            prompt = input("Enter image prompt: ").strip()
            size = input("Enter size (256x256, 512x512, 1024x1024) [512x512]: ").strip() or "512x512"
            filename = input("Output filename [generated.png]: ").strip() or "generated.png"
            output_path = os.path.join(os.path.dirname(__file__), filename)
            try:
                generated = generate_image(prompt, size, output_path)
                save_image_record(prompt, size, generated)
            except Exception as e:
                print("Image generation failed:", e)
        elif choice == "2":
            rows = list_images()
            if not rows:
                print("No generated images yet.")
            else:
                print("ID | prompt | size | filename | created_at")
                for r in rows:
                    print(" | ".join(str(x) for x in r))
        elif choice == "3":
            print("Bye.")
            break
        else:
            print("Invalid choice. Pick 1/2/3.")


if __name__ == "__main__":
    run_image_agent()
