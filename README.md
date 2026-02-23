# Longterm AGU

## 数据集说明

### 股票指数数据

数据源：akshare

**指数列表**：

- 上证指数 (sse_composite)

  1990-12-19 起始
  [data/stock_index_sse_composite.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/stock_index_sse_composite.csv)

- 沪深300 (csi300)

  2005-01-04 起始
  [data/stock_index_csi300.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/stock_index_csi300.csv)

- 创业板指 (chinext)

  2010-06-01 起始
  [data/stock_index_chinext.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/stock_index_chinext.csv)

- 恒生指数 (hsi)

  1990-05-14 起始
  [data/stock_index_hsi.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/stock_index_hsi.csv)

- 标普500 (sp500)

  1986-03-17 起始
  [data/stock_index_sp500.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/stock_index_sp500.csv)

- 纳斯达克 (nasdaq)

  1991-08-12 起始
  [data/stock_index_nasdaq.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/stock_index_nasdaq.csv)

**字段**：date 日期, code 代码, name 名称, open 开盘价, close 收盘价, high 最高价, low 最低价, amplitude 振幅

```
date,code,name,open,close,high,low,amplitude
2026-02-12,1,上证指数,4136.99,4134.02,4140.59,4124.13,0.4
2026-02-13,1,上证指数,4115.92,4082.07,4123.84,4079.77,1.07
```

**说明**：涨跌幅根据 open 和 close 确定（收盘价 > 开盘价为涨，反之为跌）

### 贵金属数据

数据源：akshare，上海黄金交易所（SGE）现货基准价

**说明**：

- 黄金基准价（沪金）：单位 元/克
  [data/precious_metal_gold.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/precious_metal_gold.csv)
- 白银基准价（沪银）：单位 元/千克
  [data/precious_metal_silver.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/precious_metal_silver.csv)

**字段**：date 交易时间, evening_price 晚盘价, morning_price 早盘价

```
date,evening_price,morning_price
2026-02-10,1125.69,1122.55
2026-02-11,1123.27,1124.87
```

### 财经早餐新闻

数据源：东方财富财经早餐，经 Firecrawl 提取后，用 gemini-3-flash-preview 总结成逐条摘要

**文件**：[data/news_breakfast.csv](https://github.com/z0gSh1u/longterm-agu/blob/master/data/news_breakfast.csv)

**字段**：date 发布日期, summary AI摘要, source_url 原文链接, source 数据来源（目前固定为 eastmoney_cjzc）

```
date,summary,source_url,source
2026-02-13,沪电股份拟投资约33亿元新建高端印制电路板生产项目，满足高速运算需求。,http://finance.eastmoney.com/a/202602123649542913.html,eastmoney_cjzc
2026-02-13,AI初创公司Anthropic完成300亿美元融资，估值达到3800亿美元。,http://finance.eastmoney.com/a/202602123649542913.html,eastmoney_cjzc
```

## 数据更新

### 金融数据获取 (price-grep)

增量更新主要股指和贵金属价格数据：

```bash
uv run price-grep
```

### 财经新闻采集 (news-read)

增量采集并总结东方财富财经早餐：

```bash
uv run news-read
```

环境变量需在中 `.env` 配置，参考 `.env.example`。

### 日历事件管理 (calendar-tool)

管理投资事件日历（财报、央行会议、政策发布等）：

```bash
# 添加事件
uv run calendar-tool add --date 2026-03-20 --event "美联储利率决议" --category macro

# 查看未来 14 天事件
uv run calendar-tool upcoming --days 14

# 按日期范围查询
uv run calendar-tool query --from 2026-03-01 --to 2026-03-31

# 删除事件
uv run calendar-tool remove --id 1
```

事件分类：`macro`（宏观）、`policy`（政策）、`earnings`（财报）、`geopolitical`（地缘）、`market`（市场）、`other`

## 投资分析 Skills

本项目集成了两个 Skills，可在支持 Agent Skills 的 AI 编程助手（如 Claude Code、OpenCode）中触发对话式投资分析。**所有分析仅供参考，不构成投资建议。**

在项目目录中启动 Claude Code，Skills 位于 `.claude/skills/`，会自动发现并按需加载。

### 生成投资报告

触发 investment-analysis Skill 即可生成今日投资报告，并保存到 `docs/reports/`：

```
/investment-analysis
```

默认包含市场概览、技术面分析、消息面解读、跨市场联动、前瞻研判、风险提示等内容。示例如 [2026-02-23-daily.md](./docs/reports/2026-02-23-daily.md)。

### 事件日历管理

触发 calendar-management Skill 可管理投资事件日历：

```
/calendar-management 帮我添加一个日历事件：3月20日美联储利率决议
/calendar-management 从近三天的新闻中提取有明确日期的事件，并加入日历
```

## License

MIT
