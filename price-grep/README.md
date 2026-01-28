# price-grep

金融数据获取工具，基于 Python + [akshare](https://github.com/akfamily/akshare)，通过 GitHub Actions 实现每日自动更新。

## 快速开始

```bash
# 安装依赖
uv sync

# 全量获取历史数据
uv run python -m src.main --mode full

# 增量更新（每日运行）
uv run python -m src.main --mode daily
```

## 数据说明

### 股票指数

| 文件名                          | 指数     |
| ------------------------------- | -------- |
| `stock_index_sse_composite.csv` | 上证指数 |
| `stock_index_csi300.csv`        | 沪深300  |
| `stock_index_chinext.csv`       | 创业板指 |
| `stock_index_hsi.csv`           | 恒生指数 |
| `stock_index_sp500.csv`         | 标普500  |
| `stock_index_nasdaq.csv`        | 纳斯达克 |

| 列名      | 说明     |
| --------- | -------- |
| date      | 交易日期 |
| code      | 指数代码 |
| name      | 指数名称 |
| open      | 开盘价   |
| close     | 收盘价   |
| high      | 最高价   |
| low       | 最低价   |
| amplitude | 振幅(%)  |

示例（`stock_index_sse_composite.csv`）：

```csv
date,code,name,open,close,high,low,amplitude
2026-01-26,000001,上证指数,4144.78,4132.61,4160.99,4124.7,0.88
2026-01-27,000001,上证指数,4125.22,4139.9,4158.8,4101.83,1.38
2026-01-28,000001,上证指数,4150.22,4151.24,4170.15,4138.02,0.78
```

### 贵金属

| 文件名                      | 品种 | 单位    |
| --------------------------- | ---- | ------- |
| `precious_metal_gold.csv`   | 黄金 | 元/克   |
| `precious_metal_silver.csv` | 白银 | 元/千克 |

| 列名          | 说明       |
| ------------- | ---------- |
| date          | 交易日期   |
| evening_price | 晚盘基准价 |
| morning_price | 早盘基准价 |

数据来源：上海黄金交易所

示例（`precious_metal_gold.csv`）：

```csv
date,evening_price,morning_price
2026-01-22,1110.56,1109.42
2026-01-25,1142.06,1138.96
2026-01-26,1143.87,1138.22
```

## 目录结构

```
price-grep/
├── src/
│   ├── main.py       # 命令行入口
│   ├── fetcher.py    # 数据获取
│   └── storage.py    # 数据存储
├── data/             # CSV 数据文件
└── example/          # 示例代码
```

## 自动更新

GitHub Actions 每日北京时间 06:00 自动运行增量更新，有新数据时自动 commit。
