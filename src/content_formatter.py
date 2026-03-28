"""HTML content formatting and sanitization for Kindle EPUB."""

import re


# Tags safe for Kindle rendering
ALLOWED_TAGS = {
    "p", "br", "h1", "h2", "h3", "h4",
    "strong", "b", "em", "i", "u",
    "ul", "ol", "li",
    "blockquote", "code", "pre",
    "a", "hr", "span", "div",
    "table", "tr", "td", "th", "thead", "tbody",
}

ALLOWED_ATTRS = {"a": {"href"}, "span": {"class"}, "div": {"class"}, "p": {"class"}}


def sanitize_html(html: str) -> str:
    """Strip unsafe tags while preserving content. Simple regex-based approach."""
    # Remove script and style blocks entirely
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML comments
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    # Remove event handlers (onclick, onload, etc.)
    html = re.sub(r'\s+on\w+\s*=\s*"[^"]*"', "", html, flags=re.IGNORECASE)
    html = re.sub(r"\s+on\w+\s*=\s*'[^']*'", "", html, flags=re.IGNORECASE)
    return html.strip()


def format_article(title: str, content_html: str, source: str, url: str = "") -> str:
    """Format a single article as HTML suitable for EPUB chapter."""
    link = f' — <a href="{url}">Read original</a>' if url else ""
    return f"""<h2>{title}</h2>
<p class="source-attribution">Source: {source}{link}</p>
{sanitize_html(content_html)}"""
