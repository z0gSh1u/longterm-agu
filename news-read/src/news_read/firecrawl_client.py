from __future__ import annotations

from dataclasses import dataclass

from firecrawl import Firecrawl


@dataclass(frozen=True)
class FirecrawlText:
    markdown: str


def fetch_markdown(api_key: str, url: str) -> FirecrawlText:
    client = Firecrawl(api_key=api_key)
    result = client.scrape(url, formats=["markdown"])

    markdown = None
    if isinstance(result, dict):
        markdown = result.get("markdown")
    else:
        markdown = getattr(result, "markdown", None)

    if not markdown:
        raise ValueError("Firecrawl returned empty markdown")

    return FirecrawlText(markdown=markdown)
