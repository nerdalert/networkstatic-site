#!/usr/bin/env python3
"""Render DOT sources to Git-friendly SVG and 2000px-wide PNGs.

Requires Graphviz (`dot`) and Pillow (`python3 -m pip install pillow`).
All exported SVGs and PNGs are derived; edit diagrams/*.dot instead.
"""
from pathlib import Path
import subprocess
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "diagrams"
ASSETS = ROOT / "assets"
TARGET_WIDTH = 2000


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    inputs = sorted(SOURCES.glob("*.dot"))
    if not inputs:
        raise SystemExit("No diagrams/*.dot sources found")
    for source in inputs:
        svg = ASSETS / f"{source.stem}.svg"
        png = ASSETS / f"{source.stem}.png"
        # Graphviz emits deterministic vector geometry from the checked-in source.
        subprocess.run(["dot", "-Tsvg", str(source), "-o", str(svg)], check=True)
        subprocess.run(["dot", "-Tpng", "-Gdpi=220", str(source), "-o", str(png)], check=True)
        with Image.open(png) as src:
            src.load()
            h = round(src.height * TARGET_WIDTH / src.width)
            if src.width != TARGET_WIDTH:
                src = src.resize((TARGET_WIDTH, h), Image.Resampling.LANCZOS)
            # RGB avoids unexpected transparency in blog themes.
            src.convert("RGB").save(png, "PNG", optimize=True)
        with Image.open(png) as img:
            print(f"{png.relative_to(ROOT)}  {img.width}×{img.height}  {png.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
