import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)
api_key = 'ollama'
google_api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    print(f"Ollama API Key exists and begins {api_key[:5]}")
else:
    print("Ollama API Key not set")
if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

OLLAMA_BASE_URL = "http://localhost:11434/v1"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)

system_message = "You are a helpful assistant that responds in markdown without code blocks"

def stream_ollama(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    stream = ollama.chat.completions.create(model="qwen2.5-coder:1.5b", messages=messages,stream=True)
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def stream_gemini(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    stream = gemini.chat.completions.create(model="gemini-3.5-flash", messages=messages,stream=True)
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def stream_model(prompt, model):
    if model=="Ollama":
        result = stream_ollama(prompt)
    elif model=="Gemini":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result

message_input = gr.Textbox(label="Your message:", info="Enter a message for qwen2.5-coder:1.5b", lines=7)
model_selector = gr.Dropdown(["Ollama", "Gemini"], label="Select model", value="Ollama")
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_model,
    title="LLMs",
    inputs=[message_input,model_selector],
    outputs=[message_output],
    examples=[
        ["Explain the Transformer architecture to a layperson", "Ollama"],
        ["Explain the Transformer architecture to an aspiring AI engineer", "Gemini"]
        ],
    flagging_mode="never"
    )
view.launch(inbrowser=True)