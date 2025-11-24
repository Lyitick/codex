"""Basic import tests to detect circular dependencies."""
import importlib
import pkgutil
from pathlib import Path

import bot


def iter_modules(package) -> list[str]:
    base_path = Path(bot.__file__).parent
    modules = []
    for module in pkgutil.walk_packages([str(base_path)], prefix=f"{package}."):
        modules.append(module.name)
    return modules


def test_imports() -> None:
    """Ensure all modules import without errors."""
    for module_name in iter_modules("bot"):
        importlib.import_module(module_name)
