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
system_message = "You are a helpful assistant"

def message_gpt(prompt):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    response = ollama.chat.completions.create(model="qwen2.5-coder:1.5b", messages=messages)
    return response.choices[0].message.content
message_gpt("What is today's date?")
def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()
shout("hello")
gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(inbrowser=True)