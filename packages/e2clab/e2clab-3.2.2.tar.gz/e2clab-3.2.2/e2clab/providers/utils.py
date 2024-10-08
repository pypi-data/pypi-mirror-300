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
    # do not print __init__
    if "__init__" in available_services:
        available_services.remove("__init__")
    return available_services


def load_providers(provider_list: list[str]) -> dict[str, Type[Provider]]:
    """
    Dynamically loads python files containing defined service classes
    and returns requested Provider class definitions in a dictionary.
    """
    for provider in provider_list:
        try:
            import_module(f"e2clab.providers.plugins.{provider}")
        except ImportError:
            raise E2clabProviderImportError(provider)
    _loaded = Provider.get_loaded_providers()
    return {name: prov for name, prov in _loaded.items() if name in provider_list}
