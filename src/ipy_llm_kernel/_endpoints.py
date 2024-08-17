"""
This module provides helper functions to interact with different language models.
"""

def prompt_claude(message: str, model="claude-3-5-sonnet-20240620"):
    """
    A prompt helper function that sends a message to anthropic
    and returns only the text response.

    Example models: claude-3-5-sonnet-20240620 or claude-3-opus-20240229
    """
    from anthropic import Anthropic

    # convert message in the right format if necessary
    if isinstance(message, str):
        message = [{"role": "user", "content": message}]

    # setup connection to the LLM
    client = Anthropic()

    message = client.messages.create(
        max_tokens=4096,
        messages=message,
        model=model,
    )

    # extract answer
    return message.content[0].text


def prompt_chatgpt(message: str, model="gpt-4o-2024-08-06"):
    """A prompt helper function that sends a message to openAI
    and returns only the text response.
    """
    # convert message in the right format if necessary
    import openai
    if isinstance(message, str):
        message = [{"role": "user", "content": message}]

    # setup connection to the LLM
    client = openai.OpenAI()

    # submit prompt
    response = client.chat.completions.create(
        model=model,
        messages=message
    )

    # extract answer
    return response.choices[0].message.content




def prompt_ollama(message: str, model="llama3:8b"):
    """A prompt helper function that sends a message to ollama and returns only the text response."""
    import openai
    if isinstance(message, str):
        message = [{"role": "user", "content": message}]

    # setup connection to the LLM
    client = openai.OpenAI()
    client.base_url = "http://localhost:11434/v1"
    client.api_key = "none"
    response = client.chat.completions.create(
        model=model,
        messages=message
    )

    # extract answer
    return response.choices[0].message.content


def prompt_blablador(message: str, model="blablador:alias:large"):
    """A prompt helper function that sends a message to Blablador (FZ Jülich)
    and returns only the text response.
    """
    import os
    import openai

    if model.startswith("blablador:"):
        model = model[10:]

    # convert message in the right format if necessary
    if isinstance(message, str):
        message = [{"role": "user", "content": message}]

    # setup connection to the LLM
    client = openai.OpenAI()
    client.base_url = "https://helmholtz-blablador.fz-juelich.de:8000/v1"

    # todo: enter your API key here:
    # client.api_key = ""
    client.api_key = os.environ.get('BLABLADOR_API_KEY')
    response = client.chat.completions.create(
        model=model,
        messages=message
    )

    # extract answer
    return response.choices[0].message.content

class Memory:
    chat_history = []


def prompt_with_memory(message: str, prompt: callable = prompt_chatgpt):
    # convert message in the right format and store it in memory
    question = {"role": "user", "content": message}
    Memory.chat_history.append(question)

    # receive answer
    response = prompt(Memory.chat_history)

    # convert answer in the right format and store it in memory
    answer = {"role": "assistant", "content": message}
    Memory.chat_history.append(answer)

    return response