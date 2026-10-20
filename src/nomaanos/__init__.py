from __future__ import annotations

__version__ = "6.0.0"
__all__ = ["__version__", "main"]


def main() -> int:
    from nomaanos.cli import main_cli

    return main_cli()
