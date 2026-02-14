import importlib
from pathlib import Path

from dishka import Provider


class ProviderRegistry:
    _SRC_DIR = Path("src")

    def __init__(self) -> None:
        self._providers: dict[str, Provider] = {}

    def register(self, provider_class: type) -> type:
        self._providers[provider_class.__module__] = provider_class()
        return provider_class

    def _find_potential_modules(self) -> list[str]:
        modules = []
        for injector_dir in self._SRC_DIR.rglob("injector"):
            provider_file = next(injector_dir.glob("*_provider.py"), None)
            if provider_file:
                relative = provider_file.relative_to(self._SRC_DIR.parent)
                module = ".".join(relative.with_suffix("").parts)
                modules.append(module)
        return modules

    def register_providers(self) -> None:
        for module_name in self._find_potential_modules():
            if module_name not in self._providers:
                try:
                    importlib.import_module(module_name)
                except ImportError:
                    pass

    def get_registered_providers(self) -> list[Provider]:
        return list(self._providers.values())


_registry = ProviderRegistry()


def register_provider(cls: type) -> type:
    return _registry.register(cls)


def register_providers() -> None:
    _registry.register_providers()


def get_registered_providers() -> list[Provider]:
    return _registry.get_registered_providers()
