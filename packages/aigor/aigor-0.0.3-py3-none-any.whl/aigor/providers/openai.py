# pylint: disable=R0801

"""Defines the OpenAI provider."""

from typing import Any, no_type_check
import logging
from openai import OpenAI

@no_type_check
def openai_api_request(
    user_prompt: str,
    system_prompt: str = "",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    model: str = "gpt-3.5-turbo"
) -> str:
    """Makes request to OpenAI API given parameters

    Parameters
    ==========
    user_prompt : str
        The user prompt.
    system_prompt: str = "",
        Prompt that prepares the model for some task.
    temperature: float = 0.7,
        How wild the model is behave. Greater values more wilder in vocabulary.
    max_tokens: int = 4096,
        Limit the tokens from the output.
    model: str = "gpt-3.5-turbo"
        Model name to request from.
    """
    # This should be fixed in input, not here.
    max_tokens = int(max_tokens)
    temperature = float(temperature)

    client = OpenAI()

    logging.debug("user_prompt: %s", user_prompt)
    logging.debug("system_prompt: %s", system_prompt)
    logging.debug("temperature: %s", temperature)
    logging.debug("max_tokens: %s", max_tokens)
    logging.debug("model: %s", model)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )

    content = response.choices[0].message.content if response.choices else ""

    return content


@no_type_check
def run(data: str, config: dict[str, Any]) -> str:
    """Executes the OpenAI provider."""
    # Here we will cleanup only the valid config args.
    logging.debug("config: %s", config)
    valid_args = ['system_prompt', 'temperature', 'max_tokens', 'model']
    cleaned_config = {k: v for k, v in config.items() if k in valid_args}
    logging.debug("cleaned_config: %s", cleaned_config)
    user_prompt = data
    result = openai_api_request(user_prompt, **cleaned_config)
    return result
