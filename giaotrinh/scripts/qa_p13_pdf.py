"""Render every candidate page; retain a focused P13 preview for visual audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pymupdf
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Cam_nang_devops.candidate.pdf"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", type=Path, default=ROOT / ".p13-preview")
    args = parser.parse_args()
    out = args.preview.resolve()
    if not out.is_relative_to(ROOT):
        raise ValueError("preview must be inside giaotrinh")
    out.mkdir(parents=True, exist_ok=True)
    # Clear only images produced by this focused QA tool in its verified folder.
    for pattern in ("page-*.png", "contact-*.png"):
        for stale in out.glob(pattern):
            stale.unlink()
    manifest = []
    with pymupdf.open(PDF) as doc:
        toc = doc.get_toc()
        part = next(item[2] for item in toc if item[1].startswith("PHẦN XIII"))
        answers = next(item[2] for item in toc if item[1] == "Lời giải Phần XIII")
        old_answers = next(item[2] for item in toc if item[1] == "Lời giải")
        focus = set(range(part, old_answers)) | set(range(answers, len(doc) + 1))
        thumb_pages = []
        for page_no, page in enumerate(doc, 1):
            matrix = pymupdf.Matrix(1.4, 1.4) if page_no in focus else pymupdf.Matrix(1, 1)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            # Every page is actually rasterized. Only focus pages are retained.
            if page_no in focus:
                path = out / f"page-{page_no:03d}.png"
                pix.save(path)
                with Image.open(path) as img:
                    thumb = ImageOps.contain(img.convert("RGB"), (480, 680))
                    tile = Image.new("RGB", (500, 720), "white")
                    tile.paste(thumb, ((500 - thumb.width) // 2, 20))
                    ImageDraw.Draw(tile).text((10, 695), f"PDF page {page_no}", fill="black")
                    thumb_pages.append(tile)
            text = page.get_text()
            manifest.append({"page": page_no, "rendered_pixels": [pix.width, pix.height],
                             "text_chars": len(text), "drawings": len(page.get_drawings()),
                             "focus": page_no in focus})
        for start in range(0, len(thumb_pages), 4):
            group = thumb_pages[start:start + 4]
            sheet = Image.new("RGB", (1000, 1440), "#dddddd")
            for j, tile in enumerate(group):
                sheet.paste(tile, ((j % 2) * 500, (j // 2) * 720))
            sheet.save(out / f"contact-{start // 4 + 1:02d}.png")
    (out / "render_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"RENDERED_ALL pages={len(manifest)} focused={len(focus)} sheets={(len(thumb_pages) + 3) // 4}")
    print(f"PREVIEW {out}")


if __name__ == "__main__":
    main()
