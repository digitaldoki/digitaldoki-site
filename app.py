import os
import gradio as gr
from openai import OpenAI

# Prompts
kids_prompt = """
You are Doki, a playful and wise lion mascot.
Rules:
1. Always be safe, friendly, and encouraging.
2. Never discuss violence, self-harm, adult themes, or unsafe behaviors.
3. If asked about unsafe topics, gently redirect:
   "🦁 That’s a little too heavy for me, friend. Let’s talk about something brighter!"
4. Encourage curiosity with safe, educational, or fun answers (animals, learning, coding basics, creativity).
5. Always stay in character: playful, caring, and wise — like a fun lion friend.
"""

caregiver_prompt = """
You are Doki, a playful but wise lion mascot who helps caregivers and families.
Rules:
1. You may discuss resources for caregivers, therapy options, productivity, and education.
2. Always be safe, respectful, and encouraging — no adult/unsafe content.
3. If asked unsafe/illegal things, redirect safely.
4. Maintain warmth and lion character, but you can recommend helpful tools and resources (planners, therapy apps, affiliate links).
"""

# Safety filter
blocked_keywords = ["kill", "suicide", "sex", "porn", "drugs", "violence", "gun", "murder", "blood", "self-harm"]

def is_safe_input(user_input):
    lowered = user_input.lower()
    return not any(word in lowered for word in blocked_keywords)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Free chat limiter
MAX_FREE_MESSAGES = 5
user_messages = {}

# Chat function
def chat_with_doki(message, history, mode="kids", username="guest"):
    count = user_messages.get(username, 0)
    if count >= MAX_FREE_MESSAGES:
        return "🦁 Roar! You've reached the free chat limit. Support Doki 👉 https://www.buymeacoffee.com/digitaldoki"
    user_messages[username] = count + 1

    if not is_safe_input(message):
        return "🦁 That’s a little too heavy for me, friend. Let’s talk about something brighter!"

    system_prompt = kids_prompt if mode == "kids" else caregiver_prompt
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"🦁 Error: {str(e)}"

# Gradio UI with pill toggle
theme = gr.themes.Soft(primary_hue="yellow", secondary_hue="indigo").set(
    body_background_fill="linear-gradient(135deg, #FFD700, #1E3A8A, #FF4FD8)"
)

with gr.Blocks(theme=theme, css="""
  .pill-toggle input[type="radio"] {display:none;}
  .pill-toggle label {
    display:inline-block;
    padding:10px 20px;
    border-radius:25px;
    margin:5px;
    font-weight:bold;
    cursor:pointer;
    transition:all 0.3s ease;
  }
  .pill-toggle input[type="radio"]:checked+label {
    background:#FFD700;
    color:black;
    box-shadow:0 4px 10px rgba(0,0,0,0.2);
  }
""") as demo:
    gr.Markdown("## 🦁 DigitalDoki Chat — Your Playful & Wise Lion Guide")
    mode_selector = gr.Radio(choices=["kids", "caregiver"], value="kids", label="Choose Chat Mode 🦁", elem_classes="pill-toggle")
    gr.ChatInterface(fn=chat_with_doki, additional_inputs=[mode_selector])

if __name__ == "__main__":
    demo.launch()
