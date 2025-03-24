import os
import openai
import gradio as gr

# Läs in API-nyckeln från miljövariabel
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_agent(message, history):
    try:
        messages = []

        # Lägg till historik i OpenAI-format
        for h in history:
            if "role" in h and "content" in h:
                messages.append({"role": h["role"], "content": h["content"]})

        messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"⚠️ Fel: {str(e)}"

# Skapa Gradio UI
chat = gr.ChatInterface(
    fn=ask_agent,
    title="Minimal GPT-3.5 Agent",
    chatbot=gr.Chatbot(type="messages")
)

if __name__ == "__main__":
    # Render sätter port i miljövariabeln PORT (default till 7860 om du kör lokalt)
    port = int(os.environ.get("PORT", 7860))
    chat.launch(server_name="0.0.0.0", server_port=port)
