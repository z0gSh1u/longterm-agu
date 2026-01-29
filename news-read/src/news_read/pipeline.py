from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .akshare_client import (
    BreakfastLink,
    get_breakfast_links,
    get_latest_breakfast_link,
)
from .firecrawl_client import fetch_markdown
from .llm_client import LlmConfig, split_news_summaries
from .storage import NewsItem, append_news_items


@dataclass(frozen=True)
class PipelineConfig:
    firecrawl_api_key: str
    llm_config: LlmConfig
    data_dir: str


def _process_link(config: PipelineConfig, link: BreakfastLink) -> list[NewsItem]:
    markdown = fetch_markdown(config.firecrawl_api_key, link.url).markdown
    summaries = split_news_summaries(config.llm_config, markdown)
    items = [
        NewsItem(date=link.date, summary=summary, source_url=link.url)
        for summary in summaries
    ]
    return items


def run_daily(config: PipelineConfig) -> str:
    latest = get_latest_breakfast_link()
    if latest is None:
        raise ValueError("No breakfast link found from AKShare")

    items = _process_link(config, latest)
    csv_path = append_news_items(config.data_dir, items)
    return str(csv_path)


def run_history(config: PipelineConfig) -> str:
    links = list(get_breakfast_links())
    if not links:
        raise ValueError("No breakfast links found from AKShare")

    all_items: list[NewsItem] = []
    for link in links:
        items = _process_link(config, link)
        all_items.extend(items)

    csv_path = append_news_items(config.data_dir, all_items)
    return str(csv_path)
