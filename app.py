import os
import gradio as gr
from openai import OpenAI

# --- Lubby Llama Prompt ---
SYSTEM_PROMPT = """
You are Lubby Llama, the Patch Day Drama AI helper.
Rules:
1. Help players troubleshoot Sims-style mod and patch issues.
2. Always suggest safe fixes (update mods, clear cache, repair game).
3. Never suggest pirated or unsafe content.
4. Be playful, supportive, and llama-themed in tone.
"""

# --- Initialize OpenAI client ---
# Uses OPENAI_API_KEY from Hugging Face "Secrets"
client = OpenAI()

# --- Free message limiter ---
MAX_FREE_MESSAGES = 5
user_messages = {}


def chat_with_lubby(message, history, username="guest"):
    """Main chat function for Lubby Llama"""
    count = user_messages.get(username, 0)
    if count >= MAX_FREE_MESSAGES:
        return (
            "🦙 You've hit the free chat limit.\n\n"
            "Support Patch Day Drama 👉 https://www.buymeacoffee.com/patchdaydrama"
        )

    user_messages[username] = count + 1

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cheap & fast model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="green", secondary_hue="purple")) as demo:
    gr.Markdown("## 🦙 Patch Day Drama — Lubby Llama to the Rescue!")
    gr.ChatInterface(fn=chat_with_lubby)

# --- Launch App ---
if __name__ == "__main__":
    demo.launch()
