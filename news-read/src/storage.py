"""
数据存储模块 - CSV 文件的读写和增量更新
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent.parent / "data"


@dataclass(frozen=True)
class NewsItem:
    date: str
    summary: str
    source_url: str
    source: str = "eastmoney_cjzc"


def get_data_path() -> Path:
    return DATA_DIR / "news_breakfast.csv"


def save_full_history(items: list[NewsItem]) -> None:
    file_path = get_data_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame([item.__dict__ for item in items])
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"  已保存到 {file_path} ({len(df)} 条记录)")


def append_daily_data(items: list[NewsItem]) -> int:
    file_path = get_data_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    new_df = pd.DataFrame([item.__dict__ for item in items])
    if new_df.empty:
        return 0

    if not file_path.exists():
        save_full_history(items)
        return len(new_df)

    old_df = pd.read_csv(file_path, encoding="utf-8-sig")
    merged = pd.concat([old_df, new_df], ignore_index=True)
    merged = merged.drop_duplicates(subset=["date", "summary"], keep="first")

    new_count = len(merged) - len(old_df)
    if new_count > 0:
        merged.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"  新增 {new_count} 条记录")
    else:
        print("  无新数据")

    return new_count
