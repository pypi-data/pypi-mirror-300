"""Defines the anthropic provider."""

from typing import Any
import logging
from anthropic import Anthropic
from anthropic.types import TextBlock, ToolUseBlock



def claude_api_request(
    user_prompt: str,
    system_prompt: str = "",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    model: str = "claude-3-sonnet-20240229"
) -> str:
    """Makes request o Anthropic API given parameters

    Parameters
    ==========
    user_prompt : str
        The user prompt.
    system_prompt: str = "",
        Prompt that prepares the model for some task.
    temperature: float = 0.7,
        How wild the model is behave. Greater values more wilder in vocabulary.
    max_tokens: int = 4096,
        Limt the tokens from the output.
    model: str = "claude-3-sonnet-20240229"
        Model name to request from.
    """
    # This should be fixed in input, not here.
    max_tokens = int(max_tokens)
    temperature = float(temperature)

    client = Anthropic()

    logging.debug("user_prompt: %s", user_prompt)
    logging.debug("system_prompt: %s", system_prompt)
    logging.debug("temperature: %s", temperature)
    logging.debug("max_tokens: %s", max_tokens)
    logging.debug("model: %s", model)
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
        ]
    )

    content: str = ""
    if message.content:
        first_block = message.content[0]
        if isinstance(first_block, TextBlock):
            content = first_block.text
        elif isinstance(first_block, ToolUseBlock):
            logging.debug("First block %s", dir(first_block))

    return content


def run(data: str, config: dict[str, Any]) -> str:
    """Executes the anthropic provider."""
    # HEre we will cleanup only the valid config args.
    logging.debug("config: %s", config)
    valid_args = ['system_prompt', 'temperature', 'max_tokens', 'model']
    cleaned_config = {k: v for k, v in config.items() if k in valid_args}
    logging.debug("cleaned_config: %s", cleaned_config)
    user_prompt = data
    result = claude_api_request(user_prompt, **cleaned_config)
    return result
