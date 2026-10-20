from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


class EnclaveDocGenerator:
    """
    NomaanOS Automated Architecture & API Documentation Generator.
    Parses Python ASTs across the monorepo to extract module docstrings
    and auto-generate live architecture catalogs.
    """

    def __init__(
        self, src_dir: str = "src", output_file: str = "docs/MODULES_CATALOG.md"
    ) -> None:
        self.src_dir = Path(src_dir)
        self.output_path = Path(output_file)

    def scan_modules(self) -> list[dict[str, Any]]:
        catalog: list[dict[str, Any]] = []
        if not self.src_dir.is_dir():
            return catalog

        for py_path in sorted(self.src_dir.glob("*.py")):
            try:
                tree = ast.parse(py_path.read_text(encoding="utf-8"))
                docstring = ast.get_docstring(tree) or "No module docstring specified."
                classes = [
                    n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)
                ]

                catalog.append(
                    {
                        "module": py_path.name,
                        "docstring": docstring.strip(),
                        "classes": classes,
                    }
                )
            except (SyntaxError, OSError):
                continue

        return catalog

    def generate_documentation_catalog(self) -> dict[str, Any]:
        modules = self.scan_modules()
        lines = [
            "# NomaanOS-Core Subsystem Catalog",
            "",
            f"**Total Audited Modules:** {len(modules)}",
            "",
            "| Module | Classes | Description |",
            "| :--- | :--- | :--- |",
        ]

        for m in modules:
            cls_str = ", ".join(m["classes"]) if m["classes"] else "None"
            desc = m["docstring"].split("\n")[0].replace("|", "-")
            lines.append(f"| `{m['module']}` | `{cls_str}` | {desc} |")

        content = "\n".join(lines) + "\n"

        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            self.output_path.write_text(content, encoding="utf-8")
        except OSError:
            pass

        return {
            "status": "DOCUMENTATION_CATALOG_GENERATED",
            "modules_indexed": len(modules),
            "output_path": str(self.output_path),
        }


if __name__ == "__main__":
    generator = EnclaveDocGenerator()
    print("Doc Generator:", generator.generate_documentation_catalog())
