import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)
api_key = 'ollama'
if api_key:
    print(f"Ollama API Key exists and begins {api_key[:5]}")
else:
    print("Ollama API Key not set")
"""openai = OpenAI()"""
OLLAMA_BASE_URL = "http://localhost:11434/v1"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')
system_message = "You are a helpful assistant that responds in markdown without code blocks"

message_input = gr.Textbox(label="Your message:", info="Enter a message for qwen2.5-coder:1.5b", lines=7)
message_output = gr.Markdown(label="Response:")

def message_gpt(prompt):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    response = ollama.chat.completions.create(model="qwen2.5-coder:1.5b", messages=messages)
    return response.choices[0].message.content
message_gpt("What is today's date?")
def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()
shout("hello")
view = gr.Interface(
    fn=message_gpt,
    title="GPT",
    inputs=[message_input],
    outputs=[message_output],
    examples=[
        "Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",
        ],
    flagging_mode="never"
    )
view.launch(inbrowser=True)