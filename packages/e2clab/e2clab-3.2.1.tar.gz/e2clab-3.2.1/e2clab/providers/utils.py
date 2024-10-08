"""
Utils for dynamisc imports and instanciation
"""

from importlib import import_module
from pathlib import Path
from typing import Type

from e2clab.providers import Provider
from e2clab.providers.errors import E2clabProviderImportError

# from e2clab.constants import Environment, SUPPORTED_ENVIRONMENTS


def get_available_providers() -> list[str]:
    current_dir = Path(__file__).resolve().parent
    plugins_dir = current_dir / "plugins"
    # list of plugins available
    available_services = [f.stem for f in plugins_dir.glob("*.py")]
    return available_services


def load_providers(provider_list: list[str]) -> dict[str, Type[Provider]]:
    """
    Dynamically loads python files containing defined service classes
    and returns Provider class definitions in a dictionary.
    """
    for provider in provider_list:
        try:
            import_module(f"e2clab.providers.plugins.{provider}")
        except ImportError:
            raise E2clabProviderImportError(provider)
    return Provider.get_loaded_providers()
