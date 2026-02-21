"""
数据存储模块 - CSV 文件的读写和增量更新
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent.parent.parent / "data"
ERROR_LOG_PATH = DATA_DIR / "news_read_errors.txt"


@dataclass(frozen=True)
class NewsItem:
    date: str
    summary: str
    source_url: str
    source: str = "eastmoney_cjzc"


def get_data_path() -> Path:
    return DATA_DIR / "news_breakfast.csv"


def log_error(date: str, url: str, error: str) -> None:
    ERROR_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"Date: {date}\nURL: {url}\nError: {error}\n{'-' * 40}\n")


def append_single_item(item: NewsItem) -> bool:
    file_path = get_data_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    new_df = pd.DataFrame([item.__dict__])

    if not file_path.exists():
        new_df.to_csv(file_path, index=False, encoding="utf-8-sig")
        return True

    old_df = pd.read_csv(file_path, encoding="utf-8-sig")
    merged = pd.concat([old_df, new_df], ignore_index=True)
    merged = merged.drop_duplicates(subset=["date", "summary"], keep="first")
    merged = merged.sort_values("date", ascending=True, kind='stable').reset_index(drop=True)

    if len(merged) > len(old_df):
        merged.to_csv(file_path, index=False, encoding="utf-8-sig")
        return True
    return False


def get_existing_dates() -> set[str]:
    file_path = get_data_path()
    if not file_path.exists():
        return set()
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    return set(df["date"].unique())
