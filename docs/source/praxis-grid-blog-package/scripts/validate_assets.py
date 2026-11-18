#!/usr/bin/env python3
"""Fail on missing relative image/link targets or malformed/undersized PNGs."""
from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
article = (ROOT / 'article.md').read_text()
images = re.findall(r'!\[([^\]]+)\]\(([^)]+)\)', article)
assert len(images) == 7, f'Expected 7 article images, got {len(images)}'
assert len({path for _, path in images}) == 7, 'Images repeated'
for alt, rel in images:
    assert alt.strip(), f'Empty alt text: {rel}'
    path = ROOT / rel
    assert path.is_file(), f'Missing image: {rel}'
    with Image.open(path) as im:
        im.verify()
    with Image.open(path) as im:
        assert im.format == 'PNG', rel
        assert 1600 <= im.width <= 2400, f'Wrong PNG width {rel}: {im.width}'
        print(f'OK {rel}: {im.width}×{im.height}')
    src = ROOT / 'diagrams' / (path.stem + '.dot')
    vec = ROOT / 'assets' / (path.stem + '.svg')
    assert src.is_file() and vec.is_file(), f'Missing editable source/vector for {rel}'

for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', article):
    if target.startswith(('https://', 'http://', '#', 'mailto:')):
        continue
    assert (ROOT / target).is_file(), f'Missing local link: {target}'

print('OK: seven unique images, editable diagrams, vector exports, and local Markdown links')
