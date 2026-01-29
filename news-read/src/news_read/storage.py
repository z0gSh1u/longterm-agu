from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class NewsItem:
    date: str
    summary: str
    source_url: str
    source: str = "eastmoney_cjzc"


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def append_news_items(data_dir: str, items: list[NewsItem]) -> Path:
    _ensure_dir(data_dir)
    csv_path = Path(data_dir) / "news_breakfast.csv"

    new_df = pd.DataFrame([item.__dict__ for item in items])

    if csv_path.exists():
        old_df = pd.read_csv(csv_path)
        merged = pd.concat([old_df, new_df], ignore_index=True)
        merged = merged.drop_duplicates(subset=["date", "summary"], keep="first")
        merged.to_csv(csv_path, index=False)
    else:
        new_df.to_csv(csv_path, index=False)

    return csv_path
