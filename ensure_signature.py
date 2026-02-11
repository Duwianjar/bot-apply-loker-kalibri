#!/usr/bin/env python3
from pathlib import Path
import sys

SIGNATURE = '''"""
Bot Apply Loker Kalibri
By Duwiaaw
Contact: 085157993801
Email: duwianjarariwibowo@gmail.com
Website: daaw.online
GitHub: github.com/Duwianjar
"""'''


def ensure_signature(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    if SIGNATURE in content:
        return False

    updated = f"{SIGNATURE}\n\n{content.lstrip()}"
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: ensure_signature.py <file_path>")
        return 1

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"File not found: {target}")
        return 1

    if target.name != "kalibrr_click.py":
        return 0

    changed = ensure_signature(target)
    if changed:
        print("Signature block ditambahkan otomatis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
