import os
import random
import datetime
import re
from google import genai
from dotenv import load_dotenv
import ollama # New import for Ollama

load_dotenv()

# Client and Model initialization for Gemini
client = genai.Client(api_key=os.getenv("API_KEY"))
GEMINI_MODEL_ID = "gemini-2.5-flash" # Renamed for clarity

# Ollama Model Initialization
OLLAMA_MODEL_ID = "llama3.2:1b" 

OPERATIONS = {
    "add": (["add", "sum", "+"], lambda x, y: x + y, "sum"),
    "sub": (["subtract", "minus", "-"], lambda x, y: x - y, "difference"),
    "mul": (["multiply", "*", "x"], lambda x, y: x * y, "product"),
    "div": (["divide", "/"], lambda x, y: x / y if y != 0 else "Error: Division by zero", "quotient"),
}

def get_numbers(text, count=2):
    nums = [float(s) for s in re.findall(r'-?\d+\.?\d*', text)]
    return nums[:count]

def handle_gemini(prompt,chat_history):
    try:
        gemini_contents = []
        for entry in chat_history:
            gemini_contents.append({"role": entry["role"],"parts":[{"text":entry["content"]}]})
            gemini_contents.append({"role": "user","parts":[{"text": prompt}]})

        response = client.models.generate_content(
            model=GEMINI_MODEL_ID, # Use GEMINI_MODEL_ID
            contents=gemini_contents
        )
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {e}"

# New function for Ollama
def handle_ollama(prompt,chat_history, model_id=OLLAMA_MODEL_ID):
    try:
        ollama_messages = []
        for entry in chat_history:
            role = "assistant" if entry ["role"] == "model" else entry["role"]
            ollama_messages.append({"role":role,"content":entry["content"]})
            ollama_messages.append({"role":"user","content":prompt})

            response = ollama.chat(model=model_id, messages=ollama_message)
        return response['message']['content']
    except Exception as e:
        return f"Error connecting to Ollama: {e}."

def process_request(prompt, llm_provider="gemini",chat_history=None):
    if chat_history is None:
        chat_history=[] # Added llm_provider argument
    prompt_lower = prompt.lower()

    # Math Check
    for key, (keywords, func, label) in OPERATIONS.items():
        if any(word in prompt_lower for word in keywords):
            nums = get_numbers(prompt_lower)
            if len(nums) >= 2:
                return f"The {label} is: {func(nums[0], nums[1])}"

    # Utility Checks
    if any(w in prompt_lower for w in ["toss", "flip"]):
        result = random.choice(["heads", "tails"])
        return f"The coin landed on: {result.upper()}!"

    if any(w in prompt_lower for w in ["date", "time", "now"]):
        return f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Fallback to chosen LLM
    if llm_provider == "gemini":
        response = handle_gemini(prompt,chat_history)
    elif llm_provider == "ollama":
        response = handle_ollama(prompt,chat_history)
    else:
        return "Invalid LLM provider.",chat_history
    #update history
    chat_history.append({"role":"user","content":prompt})
    chat_history.append({"role":"model","content":response})
    return response,chat_history 
    