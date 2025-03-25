import os
from mistralai import Mistral
from constants import Mistral_apikey

def get_traits_from_AI(features: dict):
    # Get the directory where THIS script (agent.py) is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

    # Correct relative path
    file_path = os.path.join(BASE_DIR, "agent.py")  

    SYSTEM_PROMPT = ""
    with open(file_path, 'r') as prompt_file:  
        SYSTEM_PROMPT = prompt_file.read()

    api_key = Mistral_apikey
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)
    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}"},
        {"role": "user", "content": f"The available features for user handwriting are: {str(features)}"},
    ]

    chat_response = client.chat.complete(model=model, messages=messages)

    return chat_response.choices[0].message.content
