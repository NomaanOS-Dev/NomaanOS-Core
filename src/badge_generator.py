import json
from pathlib import Path

class SecurityBadgeGenerator:
    """
    NomaanOS Automated Security Badge & SVG Shield Generator.
    Produces professional status badges for GitHub repository display.
    """
    def __init__(self, badge_dir: str = "docs/badges"):
        self.badge_path = Path(badge_dir)
        self.badge_path.mkdir(parents=True, exist_ok=True)

    def generate_badges(self) -> dict:
        print("\n[!] GENERATING ENTERPRISE SECURITY SHIELD BADGES...")
        print("-" * 60)
        
        secure_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="140" height="20">
  <linearGradient id="b" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>
  <mask id="a"><rect width="140" height="20" rx="3" fill="#fff"/></mask>
  <g mask="url(#a)"><path fill="#555" width="65" height="20"/><path fill="#4c1" x="65" width="75" height="20"/><path fill="url(#b)" width="140" height="20"/></g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="32.5" y="15" fill="#010101" fill-opacity=".3">nomaanos</text>
    <text x="32.5" y="14">nomaanos</text>
    <text x="101.5" y="15" fill="#010101" fill-opacity=".3">secure</text>
    <text x="101.5" y="14">secure</text>
  </g>
</svg>"""

        badge_file = self.badge_path / "security_shield.svg"
        badge_file.write_text(secure_svg)
        
        print("    --> Generated SVG Security Shield: docs/badges/security_shield.svg")
        print("-" * 60)
        print("[+] Security Badges Generated Successfully.\n")
        
        return {"status": "BADGES_GENERATED", "path": str(badge_file)}

if __name__ == "__main__":
    bg = SecurityBadgeGenerator()
    bg.generate_badges()
