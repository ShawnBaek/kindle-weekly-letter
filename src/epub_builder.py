"""Build EPUB from content JSON.

Usage:
    python3 -m src.epub_builder --input output/content.json --output output/newsletter.epub
"""

import argparse
import json
import sys
from pathlib import Path

from ebooklib import epub
from jinja2 import Environment, FileSystemLoader

from .config import TEMPLATES_DIR, STYLES_DIR


def build_epub(content: dict, output_path: Path) -> Path:
    """Build an EPUB file from content dictionary."""
    book = epub.EpubBook()

    title = content["title"]
    date = content["date"]
    sections = content["sections"]

    # Metadata
    book.set_identifier(f"kindle-letter-{date}")
    book.set_title(title)
    book.set_language("en")
    book.add_author("Kindle Weekly Letter")

    # Load CSS
    css_path = STYLES_DIR / "kindle.css"
    css_content = css_path.read_text()
    style = epub.EpubItem(
        uid="style",
        file_name="style/kindle.css",
        media_type="text/css",
        content=css_content.encode("utf-8"),
    )
    book.add_item(style)

    # Jinja2 templates
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)
    cover_tpl = env.get_template("cover.html")
    chapter_tpl = env.get_template("chapter.html")

    # Cover page
    cover_html = cover_tpl.render(
        title=title,
        date=date,
        topics=[s["topic"] for s in sections],
    )
    cover = epub.EpubHtml(
        title="Cover",
        file_name="cover.xhtml",
        content=cover_html.encode("utf-8"),
    )
    cover.add_item(style)
    book.add_item(cover)

    # Chapters
    chapters = []
    for i, section in enumerate(sections, 1):
        chapter_html = chapter_tpl.render(
            topic=section["topic"],
            intro=section.get("intro", ""),
            articles=section.get("articles", []),
        )
        ch = epub.EpubHtml(
            title=section["topic"],
            file_name=f"chapter_{i}.xhtml",
            content=chapter_html.encode("utf-8"),
        )
        ch.add_item(style)
        book.add_item(ch)
        chapters.append(ch)

    # Table of contents
    book.toc = [epub.Link("cover.xhtml", "Cover", "cover")] + [
        epub.Link(f"chapter_{i}.xhtml", s["topic"], f"chapter_{i}")
        for i, s in enumerate(sections, 1)
    ]

    # Spine (reading order)
    book.spine = ["nav", cover] + chapters

    # Navigation
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Write
    output_path.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(output_path), book)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Build EPUB from content JSON")
    parser.add_argument("--input", required=True, help="Path to content JSON file")
    parser.add_argument("--output", required=True, help="Output EPUB file path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    content = json.loads(input_path.read_text())
    output_path = build_epub(content, Path(args.output))
    print(f"EPUB created: {output_path}")


if __name__ == "__main__":
    main()
