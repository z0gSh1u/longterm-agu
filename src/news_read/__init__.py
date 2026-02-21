"""
News read package - 财经新闻采集工具
"""

from .fetcher import (
    BreakfastLink,
    fetch_markdown,
    get_breakfast_links,
    split_news_summaries,
)
from .storage import NewsItem, append_single_item, get_existing_dates

__all__ = [
    "BreakfastLink",
    "NewsItem",
    "fetch_markdown",
    "get_breakfast_links",
    "split_news_summaries",
    "append_single_item",
    "get_existing_dates",
]
