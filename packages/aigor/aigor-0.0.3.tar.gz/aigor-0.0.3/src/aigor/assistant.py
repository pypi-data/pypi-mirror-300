"""Real assistant functions."""

import shutil
import logging
from pathlib import Path
from typing import Any

import yaml
import typer

from aigor.common import (
    get_app_dir,
    config_read,
    config_write
)
from aigor.provider import provider_is_valid, provider_get_func


def assistant_name(name: str) -> str:
    """Formats assistant name given input.

    Parameters
    ==========
    name : str
        Assistant name.

    Returns
    =======
    str
        Assistant name without invalid characters.
    """
    aname = name
    aname = aname.replace(' ', '_')

    return aname


def assistant_path(name: str) -> Path:
    """Returns an cannonical path to a given assistant.

    Parameters
    ==========
    name : str
        Assistant name.

    Returns
    =======
    Path
        Full path to assistant dir.
    """
    app_dir = get_app_dir()
    assistant_dir = app_dir / assistant_name(name)
    return assistant_dir


def assistants_get() -> list[str]:
    """Get the list of installed assistants.

    Returns
    ========
    list[Path]:
        Return the list of assistants
    """
    app_dir = get_app_dir()
    assistants: list[str] = []
    if app_dir.exists():
        # For now we consider each dir inside `app_dir` as an assistant.
        assistants = [
            str(assistant.name)
            for assistant in app_dir.iterdir()
            if assistant.is_dir()
        ]

    return assistants


def assistant_config_is_valid(config: dict[str, Any]) -> bool:
    """Verifies if assistant config is valid.

    Parameters
    ==========
    name : str
        Assistant name.

    Returns
    =======
    bool
        If config is valid.
    """
    # Must contain at least `provider` and `name`
    return 'provider' in config and 'name' in config


def assistant_config_read(name: str) -> dict[str, Any]:
    """Reads config from assistant `name`.

    Parameters
    ==========
    name : str
        Assistant name.

    Returns
    =======
    dict[str, Any]
        The configuration contents. Or none if does not exists.
    """
    config: dict[str, Any] = {}
    try:
        assistant_dir = assistant_path(name)
        assistant_config = assistant_dir / "config.yaml"
        with open(assistant_config, "r", encoding="UTF-8") as file:
            config = yaml.safe_load(file)
    except (FileNotFoundError, PermissionError, IOError) as e:
        logging.error("Loading assistant %s config: %s", name, e)

    return config


def assistant_config_write(name: str, config: dict[str, Any]) -> None:
    """Writes config from assistant `name`.

    Parameters
    ==========
    name : str
        Assistant name.
    config : dict[Any]
        The config dictionary

    Returns
    =======
    None
    """
    try:
        assistant_dir = assistant_path(name)
        assistant_config = assistant_dir / "config.yaml"
        with open(assistant_config, "w", encoding="UTF-8") as file:
            yaml.dump(config, file, default_flow_style=False)
    except (FileNotFoundError, PermissionError, IOError) as e:
        logging.error("Loading assistant %s config: %s", name, e)


def assistant_is_valid(name: str) -> bool:
    """Verifies if assistant `name` is valid.

    Valid assistant must contain a valid configuration.

    Parameters
    ==========
    name : str
        Assistant name.

    Returns
    =======
    bool
        If assistant is valid.
    """
    assistant_dir = assistant_path(name)
    if not assistant_dir.is_dir():
        return False

    assistant_config_path = assistant_dir / "config.yaml"
    if not assistant_config_path.exists():
        return False

    assistant_config = assistant_config_read(name)
    if not assistant_config_is_valid(assistant_config):
        return False

    return True


def assistant_call(name: str, text: str) -> None:
    """Makes callence using the `name` assistant.

    Parameters
    =========
    name : str
        The name of the assistent to be used in callence. 
    text : str
        The text to be sent to the provider.
    """
    logging.debug("call %s", name)
    config = assistant_config_read(name)
    logging.debug("CONFIG: %s", config)
    logging.debug("TEXT: %s", text)
    provider_func = provider_get_func(config['provider'])
    if provider_func is None:
        logging.error("Provider %s not found.", config['provider'])
        raise typer.Abort()
    provider_args = config.get('provider_args', {})
    result = provider_func(text, provider_args)
    logging.debug("RESULT: %s", result)
    print(result)


def assistant_create(
    name: str,
    provider: str,
    args: dict[str, Any],
    force: bool = False,
    default: bool = False,
) -> None:
    """Creates an :robot: assistant with given `name`.

    Parameters
    ==========
    name : str
        Name of the assistant without spaces.
    provider : str
        Name of the provider
    args : dict[str, Any]
        Dictionary containing parameters to be passed to provider.
    force : bool
        If we should overwrite the assistant directory.
    default : bool
        If this assistant should be set as default.
    """
    # Check if provider is valid
    if not provider_is_valid(provider):
        logging.error("Provider {provider} not valid.")
        raise typer.Abort()

    # Build assistant_dir from config path and name
    assistant_dir = assistant_path(name)

    # If directory already exists. Do not create anything
    if assistant_dir.exists():
        if force:
            logging.info("Removing %s.", assistant_dir)
            shutil.rmtree(assistant_dir)
        else:
            logging.warning("Assistant %s already exists.", name)
            raise typer.Abort()

    # Try to create the directory. And handle issues.
    try:
        assistant_dir.mkdir(parents=True, exist_ok=True)
        logging.debug("Created directory: %s", assistant_dir)
        logging.info("Setting %s to %s", name, provider)
    except OSError as e:
        logging.error("Error while creating assistant '%s': %s",
                      assistant_name(name), e)

    config: dict[str, Any] = {
        'name': name,
        'provider': provider,
    }

    if args:
        config['provider_args'] = args

    # Create the yaml file with given configurations
    assistant_config_path = assistant_dir / "config.yaml"
    with open(assistant_config_path, "w", encoding="UTF-8") as file:
        yaml.dump(config, file, default_flow_style=False)

    if default:
        assistant_default_set(name)


def assistant_delete(name: str) -> None:
    """Delete assistant named `name` (if it exists).

    Parameters
    ==========
    name : str
        Name of the assistant.
    """
    assistant_dir = assistant_path(name)
    if assistant_dir.exists() and assistant_dir.is_dir():
        try:
            shutil.rmtree(assistant_dir)
            logging.info("Assistant %s deleted.", name)
        except OSError as e:
            logging.error("ERROR: deleting assistant %s: %s", name, e)


def assistant_list() -> None:
    """List available assistants and flag the default."""
    assistants = assistants_get()

    # Add a marker to default assistant
    default = assistant_default_get()
    if default in assistants:
        index = assistants.index(default)
        assistants[index] = f"{assistants[index]} (default)"

    if assistants:
        print("\n".join(assistants))
    else:
        logging.error("No assistants were created yet.")


def assistant_default_set(name: str) -> None:
    """Set a given assistant as the default.

    Parameters
    ==========
    name : str
        Name of the assistant without spaces.
    """
    config = config_read()
    if assistant_is_valid(name):
        config['default_assistant'] = name
    config_write(config)


def assistant_default_get() -> str:
    """Get the name of default assistant.

    Returns
    ========
    str
        Name of the assistant. Or None if not set
    """
    config = config_read()
    default_assistant = config.get("default_assistant", "")
    return default_assistant


def assistant_flush(name: str) -> None:
    """Flush previous conversation from `name`.

    Parameters
    ==========
    name : str
        Name of the assistant without spaces.
    """
    logging.info("Flushing %s", name)


def assistant_chat(name: str) -> None:
    """Continues a previous conversation with `name`.

    If there is no conversation. It will start a new one.

    Parameters
    ==========
    name : str
        Name of the assistant without spaces.
    """
    logging.info("Chatting with %s", name)
