#!/usr/bin/env python3
"""Convert posts from the Hakyll site layout into this Quarto project.

Usage:  python3 scripts/import-hakyll-posts.py ../site

Reads <hakyll>/blog/*.md and <hakyll>/drafts/*.md, writes
blog/<slug>/index.qmd and drafts/<slug>/index.qmd, and copies <hakyll>/images.

Changes made to each post:
  * the dashed Hakyll frontmatter fence becomes a YAML `---` fence
  * `published: YYYY-MM-DD`  ->  `date: YYYY-MM-DD`
  * `tags: a, b` (or `Category: a`)  ->  `categories: [a, b]`
  * drafts get `draft: true`
  * internal links of the form /blog/YYYY/MM/DD/slug/ become /blog/slug/
"""
import json
import re
import shutil
import sys
from pathlib import Path

FENCE = re.compile(r"^-{3,}\s*$")
DATE_LINK = re.compile(r"\]\(/blog/\d{4}/\d{2}/\d{2}/([^/)#]+)/?")


def parse(src: Path):
    lines = src.read_text(encoding="utf-8").splitlines()
    if not FENCE.match(lines[0]):
        raise SystemExit(f"{src}: expected a dashed frontmatter fence on line 1")
    meta, i = {}, 1
    while not FENCE.match(lines[i]):
        key, _, value = lines[i].partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]  # Hakyll allowed YAML-style quoting
        meta[key.strip().lower()] = value
        i += 1
    body = "\n".join(lines[i + 1 :]).lstrip("\n")
    return meta, body


def yaml_scalar(value: str) -> str:
    # JSON strings are valid YAML; this sidesteps quoting rules for titles
    # like `return :: a -> RC a`.
    return json.dumps(value, ensure_ascii=False)


def convert(src: Path, dest_root: Path, draft: bool):
    meta, body = parse(src)
    out = ["---", f"title: {yaml_scalar(meta['title'])}"]
    if "published" in meta:
        out.append(f"date: {meta['published']}")
    if "author" in meta:
        out.append(f"author: {yaml_scalar(meta['author'])}")
    tags = meta.get("tags") or meta.get("category")
    if tags:
        cats = ", ".join(yaml_scalar(t.strip()) for t in tags.split(","))
        out.append(f"categories: [{cats}]")
    if draft:
        out.append("draft: true")
    out.append("---")
    body = DATE_LINK.sub(r"](/blog/\1/", body)
    dest = dest_root / src.stem / "index.qmd"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out) + "\n\n" + body, encoding="utf-8")
    return dest


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    hakyll = Path(sys.argv[1]).resolve()
    root = Path(__file__).resolve().parent.parent
    n = 0
    for sub, draft in (("blog", False), ("drafts", True)):
        for src in sorted((hakyll / sub).glob("*.md")):
            convert(src, root / sub, draft)
            n += 1
    images = hakyll / "images"
    if images.is_dir():
        shutil.copytree(images, root / "images", dirs_exist_ok=True)
    print(f"converted {n} posts into {root}")


if __name__ == "__main__":
    main()
