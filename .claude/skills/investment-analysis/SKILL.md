# Skill: investment-analysis

Use when the user asks about market trends, investment analysis, stock indices, precious metals, or requests an investment report. Also use when the user mentions specific indices (上证, 沪深300, 创业板, 恒生, 标普500, 纳斯达克) or metals (黄金, 白银, 沪金, 沪银).

## Available Data

All data is in the `data/` directory:

### Stock Indices (daily OHLC)

| File | Index | Fields |
|------|-------|--------|
| `data/stock_index_sse_composite.csv` | 上证指数 | date, code, name, open, close, high, low, amplitude |
| `data/stock_index_csi300.csv` | 沪深300 | same |
| `data/stock_index_chinext.csv` | 创业板指 | same |
| `data/stock_index_hsi.csv` | 恒生指数 | same |
| `data/stock_index_sp500.csv` | 标普500 | same |
| `data/stock_index_nasdaq.csv` | 纳斯达克 | same |

Price direction: close > open = 涨, close < open = 跌

### Precious Metals (daily, 元/克 for gold, 元/千克 for silver)

| File | Metal | Fields |
|------|-------|--------|
| `data/precious_metal_gold.csv` | 沪金 | date, evening_price, morning_price |
| `data/precious_metal_silver.csv` | 沪银 | date, evening_price, morning_price |

### Financial News

| File | Fields |
|------|--------|
| `data/news_breakfast.csv` | date, summary, source_url, source |

Daily financial breakfast summaries from EastMoney, processed by AI.

### Calendar Events

| File | Fields |
|------|--------|
| `data/calendar.csv` | id, date, event, category, source, added_date |

Managed via `uv run calendar-tool` CLI. See calendar-manager skill.

## Analysis Workflow

When performing investment analysis, follow these steps IN ORDER:

### Step 1: Load Data

Use the Read tool to read the relevant CSV files. For recent analysis, read the last 200 lines of each file (use `offset` parameter). For long-term trend analysis, read more.

Always check the latest date in each file and note if data is stale (not updated to today).

### Step 2: Check Calendar

```bash
uv run calendar-tool upcoming --days 14
```

Review all upcoming events and their potential market impact before proceeding with analysis.

### Step 3: Technical Analysis

Based on OHLC data, analyze:

- **Trend direction**: Compare recent 5/10/20/60 trading days. Is the market trending up, down, or sideways?
- **Support & resistance**: Identify recent highs and lows, key round-number levels
- **Amplitude/Volatility**: Is volatility expanding or contracting? What does this signal?
- **Price position**: Where is current price relative to recent range? Near recent high (resistance pressure) or low (potential support)?

Compute mentally from the data:
- MA5 = average of last 5 closes
- MA10 = average of last 10 closes
- MA20 = average of last 20 closes

Note whether short-term MA is above or below long-term MA (golden cross / death cross signals).

### Step 4: News Analysis

Read recent entries from `data/news_breakfast.csv` (last 7–14 days). Identify:

- Major policy changes (fiscal stimulus, monetary easing/tightening)
- Industry-specific developments (regulatory crackdowns, sector support)
- International trade / geopolitical events (tariffs, sanctions, summits)
- Regulatory actions (IPO freezes, capital market rules)

For each key piece of news, assess: bullish / bearish / neutral for which markets?

### Step 5: Cross-Market Correlation

Compare trends across markets:

- **US → China transmission**: S&P500/NASDAQ trends often lead A-share (SSE/CSI300/ChiNext) sentiment by 1 trading day
- **Hong Kong bridge**: HSI reflects both US market overnight moves and China fundamentals; useful leading indicator
- **Gold vs Equities**: Gold rising while equities fall = risk-off signal; inverse relationship is typical but not absolute
- **Silver**: More industrial demand component than gold; rising silver with stable gold = growth optimism signal

### Step 6: Forward-Looking Assessment

Combine calendar events with historical patterns:

- What upcoming events could move markets? (from calendar check in Step 2)
- How did markets historically react to similar event types?
- Seasonal patterns: Spring Festival rally/hangover, year-end window dressing, quarterly rebalancing
- Policy cycle: Where are we in the monetary/fiscal cycle? Late easing = caution, early stimulus = opportunity

Be explicit about uncertainty. Say "historically X tended to Y, but current context Z may differ."

### Step 7: Output

**For conversational analysis**: Answer the user's specific question directly. Cite specific dates, prices, and percentage moves from the data. Do not pad with unnecessary sections.

**For report generation**: Write a Markdown report to `docs/reports/YYYY-MM-DD-<type>.md` using the template below. Type is `daily`, `weekly`, or a descriptive label (e.g., `gold-analysis`).

## Report Template

Save to: `docs/reports/YYYY-MM-DD-<type>.md`

    # 投资分析报告 — YYYY-MM-DD

    ## 市场概览

    （各市场最近交易日的表现。用表格呈现：市场名称 | 收盘价 | 涨跌幅 | 振幅）

    ## 技术面分析

    （对各主要指数的趋势方向、支撑压力位、波动率变化分析。引用具体价格和日期。）

    ## 消息面解读

    （近期重要新闻摘要及其对市场的影响分析。每条新闻标注日期，评估影响：利多/利空/中性。）

    ## 跨市场联动

    （全球市场相关性分析：美股传导、港股桥梁作用、贵金属避险信号。）

    ## 未来事件与展望

    （日历中的近期事件列表 + 基于分析的前瞻研判。每个事件标注日期和潜在影响方向。）

    ## 风险提示

    （当前需关注的关键风险因素。）

    ---
    *分析仅供参考，不构成投资建议。*

## Important Rules

- Always cite specific dates and numbers from the data — never fabricate data points
- When uncertain about trends, say so explicitly — do not overfit narratives to random fluctuations
- Always include the disclaimer: 分析仅供参考，不构成投资建议
- For calendar operations, use the calendar-manager skill (via `uv run calendar-tool`)
- Data may not be updated to today — always check the latest date in the CSV and note any data lag to the user
- For long-term analysis (months/years), read more rows; for daily/weekly, last 60–200 rows is sufficient
