"""
数据获取与解析模块
- AKShare 获取财经早餐 URL
- Firecrawl 提取正文
- LLM 拆分为一句话新闻
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import akshare as ak
import pandas as pd
from dateutil.parser import parse as parse_date
from firecrawl import Firecrawl
from openai import OpenAI
import json


@dataclass(frozen=True)
class BreakfastLink:
    date: str
    url: str


def _is_url(value: object) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def _parse_date(value: object) -> str | None:
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


def _find_date_column(df: pd.DataFrame) -> str | None:
    for col in df.columns:
        name = str(col)
        if "日期" in name or "时间" in name:
            return col
    return None


def _find_url_in_row(row: pd.Series) -> str | None:
    for value in row.tolist():
        if _is_url(value):
            return str(value)
    return None


def get_breakfast_links() -> list[BreakfastLink]:
    df = ak.stock_info_cjzc_em()
    if df is None or df.empty:
        return []

    date_col = _find_date_column(df)
    links: list[BreakfastLink] = []

    for _, row in df.iterrows():
        url = _find_url_in_row(row)
        if not url:
            continue

        date_str = None
        if date_col is not None:
            date_str = _parse_date(row.get(date_col))
        if not date_str:
            date_str = _parse_date(row.iloc[0])
        if not date_str:
            date_str = datetime.utcnow().date().isoformat()

        links.append(BreakfastLink(date=date_str, url=url))

    return links


def fetch_markdown(api_key: str, url: str) -> str:
    client = Firecrawl(api_key=api_key)
    result = client.scrape(
        url,
        formats=["markdown"],
        include_tags=["#ContentBody", ".txtinfos"],
        wait_for=10000,
        only_main_content=True,
    )

    if isinstance(result, dict):
        markdown = result.get("markdown")
    else:
        markdown = getattr(result, "markdown", None)

    if not markdown:
        raise ValueError("Firecrawl returned empty markdown")

    return str(markdown)


def split_news_summaries(
    api_key: str,
    base_url: str | None,
    model: str,
    content: str,
) -> Iterable[str]:
    client = (
        OpenAI(api_key=api_key, base_url=base_url)
        if base_url
        else OpenAI(api_key=api_key)
    )

    system_prompt = (
        "你是一名财经编辑。将输入的财经早餐正文拆分为多条新闻，"
        "每条新闻输出一句话中文摘要。只输出 JSON 数组，数组元素是字符串。"
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
        temperature=0.2,
    )

    text = completion.choices[0].message.content or ""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[:-3].strip()
        elif "```" in text:
            text = text.split("```")[0].strip()

    try:
        data = json.loads(text)
        if isinstance(data, list):
            items = [str(item).strip('"').strip() for item in data]
        else:
            items = [str(data).strip('"').strip()]
    except Exception:
        items = [line.strip("-•* ") for line in text.splitlines() if line.strip()]

    return [item.strip() for item in items if item.strip()]
