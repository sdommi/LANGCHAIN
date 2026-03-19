import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

load_dotenv()


def generate_initial_draft(llm, mode, goal, recipient, tone, context, history):
    mode_text = "follow-up" if mode == "follow-up" else "proposal"
    prompt = (
        "You are an expert business writer. "
        f"Draft a professional and persuasive {mode_text} email.\n"
        f"Goal: {goal}\n"
        f"Recipient: {recipient}\n"
        f"Tone: {tone}\n"
        f"Context: {context}\n"
        f"History: {history}\n"
        "Include a clear subject line and body. Keep it concise, structured, and friendly."
    )
    result = llm.invoke(prompt)
    if hasattr(result, "text"):
        return result.text
    if hasattr(result, "response"):
        return str(result.response)
    return str(result)


def revise_draft(llm, draft, feedback, goal, recipient, tone, context, history):
    prompt = (
        "You are an expert business writer revising a draft email. "
        "Incorporate the user feedback and keep the message compelling and concise.\n"
        f"Current draft:\n{draft}\n\n"
        f"Feedback: {feedback}\n"
        f"Goal: {goal}\n"
        f"Recipient: {recipient}\n"
        f"Tone: {tone}\n"
        f"Context: {context}\n"
        f"History: {history}\n"
        "Provide the final draft with subject and body."
    )
    result = llm.invoke(prompt)
    if hasattr(result, "text"):
        return result.text
    if hasattr(result, "response"):
        return str(result.response)
    return str(result)


def run_email_proposal_agent():
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set. Add to .env or environment.")

    llm = init_chat_model("openai:gpt-4o-mini", temperature=0.7)

    print("=== Email/Proposal Drafting Agent ===")
    goal = input("Enter your goal (e.g. follow up after VC meeting): ").strip()
    recipient = input("Recipient role (e.g. VC, hiring manager, client): ").strip()
    tone = input("Tone (e.g. professional, friendly, concise): ").strip() or "professional"
    context = input("Context (optional): ").strip() or ""

    history = ""
    mode = input("Mode (follow-up/proposal): ").strip().lower() or "follow-up"
    if mode not in {"follow-up", "proposal"}:
        mode = "follow-up"
    draft = generate_initial_draft(llm, mode, goal, recipient, tone, context, history)
    print("\n--- Draft 1 ---")
    print(draft)
    print("--- End Draft 1 ---\n")

    for i in range(2, 5):
        feedback = input("Enter revision feedback (or 'done' to finish): ").strip()
        if feedback.lower() in {"done", "no", "finished"}:
            break
        history += f"\n--- Draft {i-1} ---\n{draft}\nFeedback: {feedback}\n"
        draft = revise_draft(llm, draft, feedback, goal, recipient, tone, context, history)
        print(f"\n--- Draft {i} ---")
        print(draft)
        print(f"--- End Draft {i} ---\n")

    print("Final draft complete.\n")
    print(draft)

    save = input("Save final draft to file? (y/n): ").strip().lower()
    if save in {"y", "yes"}:
        filename = input("Enter filename (default: final_email.txt): ").strip() or "final_email.txt"
        with open(filename, "w") as f:
            f.write(draft)
        print(f"Draft saved to {filename}")


if __name__ == "__main__":
    run_email_proposal_agent()
