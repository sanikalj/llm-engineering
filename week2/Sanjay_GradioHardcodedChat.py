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

def chat(message, history):
    return "bananas"
message_input = gr.Textbox(label="Your message:", info="Enter a message for qwen2.5-coder:1.5b", lines=7)
message_output = gr.Markdown(label="Response:")

view = gr.ChatInterface(fn=chat)
view.launch(inbrowser=True)