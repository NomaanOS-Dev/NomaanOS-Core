from __future__ import annotations

import platform
import shutil


def render_banner(version: str = "6.0.0-PRIME") -> str:
    """
    Renders the dynamic NomaanOS Sovereign Console Header Banner.
    """
    cols = shutil.get_terminal_size((80, 24)).columns
    art = [
        r" _   _                               _____ _____ ",
        r"| \ | |                             |  _  /  ___|",
        r"|  \| | ___  _ __ ___   __ _  __ _ _ | | | \ `--. ",
        r"| . ` |/ _ \| '_ ` _ \ / _` |/ _` | '_  | | `--. \\",
        r"| |\  | (_) | | | | | | (_| | (_| | | \ \_/\/\__/ /",
        r"\_| \_/\___/|_| |_| |_|\__,_|\__,_|_|  \___/\____/ ",
    ]

    lines: list[str] = [""]
    for row in art:
        lines.append(row.center(cols))

    tagline = f"Sovereign AI Stack (SAS) | Enclave Core {version} | Linux {platform.machine()}"
    lines.append(tagline.center(cols))
    lines.append(("=" * min(cols, 80)).center(cols))
    lines.append("")

    rendered = "\n".join(lines)
    print(rendered)
    return rendered


if __name__ == "__main__":
    render_banner()
