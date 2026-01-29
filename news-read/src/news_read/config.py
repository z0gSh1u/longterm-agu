from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    firecrawl_api_key: str
    openai_api_key: str
    openai_base_url: str | None
    openai_model: str
    data_dir: str


def load_settings() -> Settings:
    firecrawl_api_key = os.environ.get("FIRECRAWL_API_KEY", "").strip()
    openai_api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not firecrawl_api_key:
        raise ValueError("FIRECRAWL_API_KEY is required")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is required")

    openai_base_url = os.environ.get("OPENAI_BASE_URL")
    openai_model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    data_dir = os.environ.get("NEWSREAD_DATA_DIR", "data").strip()

    return Settings(
        firecrawl_api_key=firecrawl_api_key,
        openai_api_key=openai_api_key,
        openai_base_url=openai_base_url,
        openai_model=openai_model,
        data_dir=data_dir,
    )
