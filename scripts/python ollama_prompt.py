import requests
import pandas as pd

from input_for_llm import input_text_big5, input_text_eating
from prompt_eating_behavior import generate_eating_behavior_classify_prompt, generate_big5_personality_prompt, \
    generate_tips_prompt


def generate_text(prompt: str, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
    """
    Generates text using the locally running Ollama server.

    :param prompt: The input prompt for the model.
    :param model: The model name (default: "llama3.2").
    :param base_url: The URL where Ollama is running (default: "http://localhost:11434").
    :return: The generated response text.
    """
    base_url = "http://persuasive.research.cs.dal.ca/mindfuleating/ollama"
    # endpoint = f"{base_url}/api/generate"
    endpoint = f"{base_url}"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response generated.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


if __name__ == "__main__":
    # user_prompt = input("Enter your prompt: ")
    # input_text = input_text_eating
    input_text = "{'Eating Behavior': 'Balanced Food Choices', 'Dominant Big5': 'Agreeableness'}"
    user_prompt = generate_tips_prompt() + input_text
    # print("\nUser Prompt:\n", user_prompt)
    # user_prompt = "what should I do if I feel dehydrated? and no water is available"
    response = generate_text(user_prompt, "samshad/mindful-tips") # [behavior-llama3.2, big5-llama3.2, tips-llama3.2, llama3.2, llama3.3, deepseek-r1:14b, deepseek-r1:32b, deepseek-r1:70b]
    print("\nGenerated Response:\n", response)
    # ["Mindful vs. Distracted Eating", "Balanced Food Choices", "Hydration Practices"]
