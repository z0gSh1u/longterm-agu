"""
命令行入口 - 支持 full 和 daily 两种运行模式
"""

from __future__ import annotations

import argparse
import os
import sys

from .fetcher import (
    fetch_markdown,
    get_breakfast_links,
    get_latest_breakfast_link,
    split_news_summaries,
)
from .storage import NewsItem, append_daily_data, save_full_history


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"缺少环境变量: {name}")
    return value


def _process_link(
    date: str,
    url: str,
    firecrawl_key: str,
    openai_key: str,
    base_url: str | None,
    model: str,
) -> list[NewsItem]:
    markdown = fetch_markdown(firecrawl_key, url)
    summaries = split_news_summaries(openai_key, base_url, model, markdown)
    return [
        NewsItem(date=date, summary=summary, source_url=url) for summary in summaries
    ]


def run_full_mode() -> None:
    print("=" * 50)
    print("运行模式: FULL (全量获取)")
    print("=" * 50)

    firecrawl_key = _require_env("FIRECRAWL_API_KEY")
    openai_key = _require_env("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    links = get_breakfast_links()
    if not links:
        raise ValueError("未获取到财经早餐链接")

    all_items: list[NewsItem] = []
    for link in links:
        print(f"处理: {link.date} {link.url}")
        all_items.extend(
            _process_link(
                link.date, link.url, firecrawl_key, openai_key, base_url, model
            )
        )

    save_full_history(all_items)

    print("\n" + "=" * 50)
    print("全量数据获取完成!")
    print("=" * 50)


def run_daily_mode() -> None:
    print("=" * 50)
    print("运行模式: DAILY (增量更新)")
    print("=" * 50)

    firecrawl_key = _require_env("FIRECRAWL_API_KEY")
    openai_key = _require_env("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    latest = get_latest_breakfast_link()
    if latest is None:
        raise ValueError("未获取到财经早餐链接")

    items = _process_link(
        latest.date, latest.url, firecrawl_key, openai_key, base_url, model
    )
    new_count = append_daily_data(items)

    print("\n" + "=" * 50)
    print(f"每日更新完成! 新增 {new_count} 条记录")
    print("=" * 50)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="news-read",
        description="财经早餐采集工具",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "daily"],
        required=True,
        help="运行模式: full=全量获取, daily=增量更新",
    )

    args = parser.parse_args()

    try:
        if args.mode == "full":
            run_full_mode()
        elif args.mode == "daily":
            run_daily_mode()
    except Exception as exc:
        print(f"\n错误: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
