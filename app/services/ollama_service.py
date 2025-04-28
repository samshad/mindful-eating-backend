import os
import requests
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def generate_result(prompt: str, model: str):
    """
    Generates text using a locally running Ollama server.

    This function sends a prompt to the Ollama server's /api/generate endpoint using the specified model.
    The base URL of the Ollama server is retrieved from the environment variable `OLLAMA_BASE_URL`.

    Parameters:
        prompt (str): The input text prompt to generate a response for.
        model (str): The name of the Ollama model to use for generation.

    Returns:
        str: The generated response text from the model, or an error message if the request fails.
    """

    base_url = os.getenv("OLLAMA_BASE_URL")

    # endpoint = f"{base_url}/api/generate"
    endpoint = f"{base_url}"
    payload = {"model": model, "prompt": prompt, "stream": False}

    logger.info(f"Sending request to Ollama with model {model}.")

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        result = response.json().get("response", "No response generated.")
        logger.info(f"Received response from Ollama: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return f"Error: {e}"
