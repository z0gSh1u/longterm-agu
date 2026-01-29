from __future__ import annotations

import argparse

from .config import load_settings
from .llm_client import LlmConfig
from .pipeline import PipelineConfig, run_daily, run_history


def _build_pipeline_config() -> PipelineConfig:
    settings = load_settings()
    llm_config = LlmConfig(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        model=settings.openai_model,
    )
    return PipelineConfig(
        firecrawl_api_key=settings.firecrawl_api_key,
        llm_config=llm_config,
        data_dir=settings.data_dir,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="财经早餐采集")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("daily", help="抓取当日财经早餐并入库")
    subparsers.add_parser("history", help="抓取历史财经早餐并入库")

    args = parser.parse_args()
    config = _build_pipeline_config()

    if args.command == "daily":
        output = run_daily(config)
    else:
        output = run_history(config)

    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
