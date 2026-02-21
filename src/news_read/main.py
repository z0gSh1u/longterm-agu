"""
命令行入口 - 支持 full 和 daily 两种运行模式
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from .fetcher import (
    fetch_markdown,
    get_breakfast_links,
    split_news_summaries,
)
from .storage import (
    NewsItem,
    append_single_item,
    get_existing_dates,
    log_error,
)


_env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(_env_path)


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


def run() -> None:
    print("=" * 50)
    print("运行模式: 自动增量补齐")
    print("=" * 50)

    firecrawl_key = _require_env("FIRECRAWL_API_KEY")
    openai_key = _require_env("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("OPENAI_MODEL", "let-it-crash")

    links = get_breakfast_links()
    if not links:
        raise ValueError("未获取到财经早餐链接")

    existing_dates = get_existing_dates()
    links_to_process = [link for link in links if link.date not in existing_dates]

    print(f"已存在日期: {len(existing_dates)} 个")
    print(f"待处理日期: {len(links_to_process)} 个")

    if not links_to_process:
        print("所有日期已存在，无需处理")
        return

    success_count = 0
    error_count = 0
    for link in links_to_process:
        print(f"处理: {link.date} {link.url}")
        try:
            items = _process_link(
                link.date, link.url, firecrawl_key, openai_key, base_url, model
            )
            for item in items:
                if append_single_item(item):
                    success_count += 1
        except Exception as e:
            error_count += 1
            log_error(link.date, link.url, str(e))
            print(f"  错误: {e} (已记录到错误日志)")

    print("\n" + "=" * 50)
    print(f"执行完成! 成功: {success_count}, 错误: {error_count}")
    print("=" * 50)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="news-read",
        description="财经早餐采集工具",
    )

    args = parser.parse_args([])

    try:
        run()
    except Exception as exc:
        print(f"\n错误: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
