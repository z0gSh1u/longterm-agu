"""
News read package - 财经新闻采集工具
"""

from .fetcher import (
    BreakfastLink,
    fetch_markdown,
    get_breakfast_links,
    get_latest_breakfast_link,
    split_news_summaries,
)
from .storage import NewsItem, append_daily_data, save_full_history

__all__ = [
    "BreakfastLink",
    "NewsItem",
    "fetch_markdown",
    "get_breakfast_links",
    "get_latest_breakfast_link",
    "split_news_summaries",
    "save_full_history",
    "append_daily_data",
]
