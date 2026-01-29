from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import akshare as ak
import pandas as pd
from dateutil.parser import parse as parse_date


@dataclass(frozen=True)
class BreakfastLink:
    date: str
    url: str


def _is_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    return value.startswith("http://") or value.startswith("https://")


def _find_url_columns(df: pd.DataFrame) -> list[str]:
    candidates: list[str] = []
    for col in df.columns:
        series = df[col]
        if series.astype(str).str.contains(r"https?://", regex=True).any():
            candidates.append(col)
    return candidates


def _find_date_column(df: pd.DataFrame) -> str | None:
    for col in df.columns:
        name = str(col)
        if "日期" in name or "时间" in name:
            return col
    return None


def _safe_parse_date(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        dt = parse_date(text, fuzzy=True)
        return dt.date().isoformat()
    except Exception:
        return None


def get_breakfast_links() -> Iterable[BreakfastLink]:
    df = ak.stock_info_cjzc_em()
    if df is None or df.empty:
        return []

    url_columns = _find_url_columns(df)
    if not url_columns:
        return []

    date_col = _find_date_column(df)

    links: list[BreakfastLink] = []
    for _, row in df.iterrows():
        url = None
        for col in url_columns:
            value = row.get(col)
            if _is_url(value):
                url = str(value)
                break
        if not url:
            continue

        date_str = None
        if date_col is not None:
            date_str = _safe_parse_date(row.get(date_col))
        if not date_str:
            date_str = _safe_parse_date(row.iloc[0])
        if not date_str:
            date_str = pd.Timestamp.utcnow().date().isoformat()

        links.append(BreakfastLink(date=date_str, url=url))

    return links


def get_latest_breakfast_link() -> BreakfastLink | None:
    links = list(get_breakfast_links())
    if not links:
        return None

    # 按日期倒序取最新
    links.sort(key=lambda item: item.date, reverse=True)
    return links[0]
