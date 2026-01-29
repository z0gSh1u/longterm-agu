from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable

from openai import OpenAI


@dataclass(frozen=True)
class LlmConfig:
    api_key: str
    base_url: str | None
    model: str


def _build_client(config: LlmConfig) -> OpenAI:
    if config.base_url:
        return OpenAI(api_key=config.api_key, base_url=config.base_url)
    return OpenAI(api_key=config.api_key)


def split_news_summaries(config: LlmConfig, content: str) -> Iterable[str]:
    client = _build_client(config)

    system_prompt = (
        "你是一名财经编辑。将输入的财经早餐正文拆分为多条新闻，"
        "每条新闻输出一句话中文摘要。只输出 JSON 数组，数组元素是字符串。"
    )

    completion = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
        temperature=0.2,
    )

    text = completion.choices[0].message.content or ""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM output is not valid JSON") from exc

    if not isinstance(data, list):
        raise ValueError("LLM output is not a JSON array")

    summaries = [str(item).strip() for item in data if str(item).strip()]
    return summaries
