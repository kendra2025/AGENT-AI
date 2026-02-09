"""Bootstrap module to run MetaNewsX from a source checkout."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_cli_module() -> object:
    cli_path = Path(__file__).parent / "src" / "metanewsx" / "cli.py"
    spec = importlib.util.spec_from_file_location("metanewsx_cli", cli_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load MetaNewsX CLI module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    """Run the MetaNewsX CLI from source."""
    module = _load_cli_module()
    module.cli()


if __name__ == "__main__":
    main()
