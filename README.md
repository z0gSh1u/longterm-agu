# Longterm AGU

金融数据工具集合 - 价格获取和财经新闻采集

## 安装

```bash
uv sync
```

## 使用

### price-grep - 金融数据获取

获取股指和贵金属历史数据：

```bash
# 全量获取
uv run price-grep --mode full

# 增量更新
uv run price-grep --mode daily
```

### news-read - 财经新闻采集

采集东方财富财经早餐：

```bash
# 全量获取
uv run news-read --mode full

# 增量更新
uv run news-read --mode daily
```

环境变量需复制 `.env.example` 文件，重命名为 `.env` 并设置：

- `FIRECRAWL_API_KEY` - Firecrawl API 密钥
- `OPENAI_API_KEY` - OpenAI API 密钥
- `OPENAI_BASE_URL` - OpenAI 兼容的 API 地址
- `OPENAI_MODEL` - 使用的模型

## 数据目录

数据保存在 `./data/` 目录下：

- `stock_index_*.csv` - 股票指数数据
- `precious_metal_*.csv` - 贵金属数据
- `news_breakfast.csv` - 财经早餐新闻
