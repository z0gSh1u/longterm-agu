#!/bin/bash
set -e

DATA_DIR="$(dirname "$0")/../assets/data"

get_date() {
    tail -n 1 "${DATA_DIR}/$1.csv" | cut -d',' -f1
}

echo "# 数据最新日期"

echo ""
echo "## 股票指数"
echo ""
echo "| 指数 | 最新日期 |"
echo "|------|----------|"
echo "| 上证指数 | $(get_date stock_index_sse_composite) |"
echo "| 沪深300 | $(get_date stock_index_csi300) |"
echo "| 创业板指 | $(get_date stock_index_chinext) |"
echo "| 恒生指数 | $(get_date stock_index_hsi) |"
echo "| 标普500 | $(get_date stock_index_sp500) |"
echo "| 纳斯达克 | $(get_date stock_index_nasdaq) |"

echo ""
echo "## 贵金属"
echo ""
echo "| 品种 | 最新日期 |"
echo "|------|----------|"
echo "| 沪金 | $(get_date precious_metal_gold) |"
echo "| 沪银 | $(get_date precious_metal_silver) |"

echo ""
echo "## 财经新闻"
echo ""
echo "| 来源 | 最新日期 |"
echo "|------|----------|"
echo "| 东方财富财经早餐 | $(get_date news_breakfast) |"

