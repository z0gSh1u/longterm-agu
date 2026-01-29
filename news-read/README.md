# news-read

财经新闻源工具：从 AKShare 获取东方财富-财经早餐 URL，通过 Firecrawl 提取正文，交给 LLM 拆分为一句话新闻并保存到 CSV。

## 安装

使用 uv：

- `uv sync`

## 配置

设置环境变量：

- `FIRECRAWL_API_KEY`（必需）
- `OPENAI_API_KEY`（必需）
- `OPENAI_BASE_URL`（可选）
- `OPENAI_MODEL`（可选，默认 `gpt-4o-mini`）

## 运行

- 全量获取：`uv run python -m src.main --mode full`
- 每日更新：`uv run python -m src.main --mode daily`

输出 CSV：`news-read/data/news_breakfast.csv`
