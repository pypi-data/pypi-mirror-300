"""Commom utilities"""

import sys
import logging
from typing import Callable, TextIO, Any
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console
import yaml
from dotenv import load_dotenv
import typer

from aigor import __appname__


def setup_logging(verbose: bool = False) -> None:
    """Setups logging based on `verbose` flag.

    Parameters
    ==========
    verbose : bool
        If True will set logging level to DEBUG, if False will set to INFO.

    Returns
    =======
    None
    """
    if verbose:
        level = logging.DEBUG
        logging.getLogger("anthropic").setLevel(logging.DEBUG)
    else:
        level = logging.WARNING
        logging.getLogger("anthropic").setLevel(logging.WARNING)

    console = Console(file=sys.stderr)
    rich_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        markup=True,
        show_path=False,
        show_time=True,
        omit_repeated_times=False,
    )
    rich_handler.setLevel(level)

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich_handler]
    )

    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
            logger.removeHandler(handler)


def get_app_dir() -> Path:
    """Get config dir based on platform.

    Returns
    =======
    Path
        A path pointing to config dir.
    """
    app_dir = Path(typer.get_app_dir(__appname__)).resolve()
    return app_dir


def process_stdin(
        process_func: Callable[..., Any],
        input_stream: TextIO,
        output_stream: TextIO
) -> None:
    """Apply process_function into the STDIN->STDOUT stream"""
    # We need to merge the whole input in a single stream instead call
    # multiple process_func per input_Stream
    for line in input_stream:
        result = process_func(line.strip())
        output_stream.write(result + '\n')
        output_stream.flush()


def search_and_load_dotenv() -> None:
    """Loads .env file from an hierachy of locations.

    It will search in CWD, if does not exist it will look inside ${HOME}.
    """
    loaded_dotenv = False
    locations = [Path("."), Path.home()]
    for location in locations:
        logging.debug("Trying to read .env from %s", location)
        if load_dotenv(location / ".env"):
            loaded_dotenv = True
            break

    if loaded_dotenv:
        logging.debug("Loaded `.env` from %s", location)
    else:
        logging.warning("Could not find .env file.")


def args_to_dict(args: list[str]) -> dict[str, str]:
    """Converts a list of strings like "key:value" into a dictionary.

    Parameters
    ==========
    args : list[str]
        List of string in formatted as "key:value". Keys and values will be
        considered as strings. Content will be stripped.

    Returns
    =======
    dict
        A dicionary of given key and values.
    """
    args_dict = {
        key.strip(): value.strip()
        for arg in args
        for key, value in [arg.split(":")]
    } if args else {}
    return args_dict


def config_read() -> dict[str, str]:
    """Read AIgor config.

    Returns
    =======
    dict[Any]
        Dictionary containing the AIgor config.
    """
    app_dir = get_app_dir()
    config_path = app_dir / "config.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, "r", encoding="UTF-8") as file:
            config = yaml.safe_load(file)
    return config


def config_write(config: dict[str, Any]) -> None:
    """Writes dictionary to AIgor config file.

    Parameters
    ===========
    config : dict[str, Any]
        Dictionary containing the AIgor config.

    Returns
    =======
    None
    """
    app_dir = get_app_dir()
    config_path = app_dir / "config.yaml"
    with open(config_path, "w", encoding="UTF-8") as file:
        yaml.dump(config, file, default_flow_style=False)
