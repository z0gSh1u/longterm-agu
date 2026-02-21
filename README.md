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

## License

MIT
