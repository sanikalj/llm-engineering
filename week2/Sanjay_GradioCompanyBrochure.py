import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from scraper import fetch_website_links, fetch_website_contents
import gradio as gr

#Env
load_dotenv(override=True)
api_key = 'ollama'
google_api_key = os.getenv('GEMINI_API_KEY')

#API keys
if api_key:
    print(f"Ollama API Key exists and begins {api_key[:5]}")
else:
    print("Ollama API Key not set")
if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")
#URLs
OLLAMA_BASE_URL = "http://localhost:11434/v1"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)

#message
system_message = "You are a helpful assistant that responds in markdown without code blocks"

#Functions
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

def stream_brochure(company_name, url, model):
    yield ""
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += fetch_website_contents(url)
    if model=="Ollama":
        result = stream_ollama(prompt)
    elif model=="Gemini":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result

name_input = gr.Textbox(label="Company name:")
url_input = gr.Textbox(label="Landing page URL including http:// or https://")
model_selector = gr.Dropdown(["Ollama", "Gemini"], label="Select model", value="Ollama")
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_brochure,
    title="Brochure Generator",
    inputs=[name_input, url_input, model_selector],
    outputs=[message_output],
    examples=[
        ["Hugging Face", "https://huggingface.co", "GPT"],
        ["Edward Donner", "https://edwarddonner.com", "Claude"]
        ],
    flagging_mode="never"
    )
view.launch(inbrowser=True)