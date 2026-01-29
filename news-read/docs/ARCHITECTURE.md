# News Read 架构文档（简化版）

> 目标：AKShare 拿 URL → Firecrawl 抓正文 → LLM 拆成一句话新闻 → CSV 存储 → GitHub Actions 每日更新。

## 1. 模块划分

- `src/fetcher.py`：AKShare 获取链接、Firecrawl 抓正文、LLM 拆分摘要
- `src/storage.py`：CSV 全量保存与增量追加
- `src/main.py`：命令行入口（full / daily）

## 2. 数据流

1. AKShare `stock_info_cjzc_em` 返回表格
2. 解析出 URL + 日期
3. Firecrawl 抓取正文 Markdown
4. LLM 输出 JSON 数组（每项一句话）
5. 写入 `news-read/data/news_breakfast.csv`

## 3. 运行模式

- 全量：`uv run python -m src.main --mode full`
- 日更：`uv run python -m src.main --mode daily`

## 4. 配置

- `FIRECRAWL_API_KEY`（必需）
- `OPENAI_API_KEY`（必需）
- `OPENAI_BASE_URL`（可选）
- `OPENAI_MODEL`（可选，默认 `gpt-4o-mini`）

## 5. 目录结构

```
news-read/
  data/
    news_breakfast.csv
  docs/
    ARCHITECTURE.md
  src/
    __init__.py
    main.py
    fetcher.py
    storage.py
  pyproject.toml
  README.md
```
