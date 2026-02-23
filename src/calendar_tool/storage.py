"""
日历事件存储模块 - CSV 文件的 CRUD 操作
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path
from typing import cast

import pandas as pd


DATA_DIR = Path(__file__).parent.parent.parent / "data"
CALENDAR_PATH = DATA_DIR / "calendar.csv"

VALID_CATEGORIES = {"macro", "policy", "earnings", "geopolitical", "market", "other"}
VALID_SOURCES = {"manual", "news_extract"}

COLUMNS = ["id", "date", "event", "category", "source", "added_date"]


@dataclass(frozen=True)
class CalendarEvent:
    id: int
    date: str
    event: str
    category: str
    source: str
    added_date: str


def _load_df() -> pd.DataFrame:
    """加载日历 CSV，若不存在则返回空 DataFrame。"""
    if not CALENDAR_PATH.exists():
        return pd.DataFrame(columns=COLUMNS)
    df = pd.read_csv(CALENDAR_PATH, encoding="utf-8-sig")
    df["id"] = df["id"].astype(int)
    df["date"] = df["date"].astype(str)
    df["added_date"] = df["added_date"].astype(str)
    return df


def _save_df(df: pd.DataFrame) -> None:
    """保存 DataFrame 到 CSV。"""
    CALENDAR_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = df.sort_values("date", ascending=True).reset_index(drop=True)
    df.to_csv(CALENDAR_PATH, index=False, encoding="utf-8-sig")


def _next_id(df: pd.DataFrame) -> int:
    """获取下一个可用 ID。"""
    if df.empty:
        return 1
    return int(df["id"].max()) + 1  # type: ignore[arg-type]


def add_event(
    event_date: str, event: str, category: str, source: str = "manual"
) -> CalendarEvent:
    """添加一个事件，返回创建的事件。"""
    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"无效分类: {category}，可选: {', '.join(sorted(VALID_CATEGORIES))}"
        )
    if source not in VALID_SOURCES:
        raise ValueError(
            f"无效来源: {source}，可选: {', '.join(sorted(VALID_SOURCES))}"
        )

    df = _load_df()
    new_id = _next_id(df)
    today = date.today().isoformat()

    new_event = CalendarEvent(
        id=new_id,
        date=event_date,
        event=event,
        category=category,
        source=source,
        added_date=today,
    )

    new_row = pd.DataFrame([asdict(new_event)])
    df = pd.concat([df, new_row], ignore_index=True)
    _save_df(df)

    return new_event


def remove_event(event_id: int) -> bool:
    """删除指定 ID 的事件，返回是否成功。"""
    df = _load_df()
    if event_id not in df["id"].values:
        return False

    df = cast(pd.DataFrame, df[df["id"] != event_id])
    _save_df(df)
    return True


def query_events(date_from: str, date_to: str) -> list[CalendarEvent]:
    """查询日期范围内的事件（含两端）。"""
    df = _load_df()
    if df.empty:
        return []

    mask = (df["date"] >= date_from) & (df["date"] <= date_to)
    filtered = cast(pd.DataFrame, df[mask]).sort_values("date")

    return [
        CalendarEvent(**{str(k): v for k, v in row.items()})
        for row in filtered.to_dict("records")
    ]


def upcoming_events(days: int = 14) -> list[CalendarEvent]:
    """查询从今天起未来 N 天的事件。"""
    today = date.today()
    date_from = today.isoformat()
    date_to = (today + timedelta(days=days)).isoformat()
    return query_events(date_from, date_to)
