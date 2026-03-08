#!/bin/bash
set -e

BASE_URL="https://zxuuu.link/longterm-agu/data"
DATA_DIR="$(dirname "$0")/../assets/data"

FILES=(
    "stock_index_sse_composite.csv"
    "stock_index_csi300.csv"
    "stock_index_chinext.csv"
    "stock_index_hsi.csv"
    "stock_index_sp500.csv"
    "stock_index_nasdaq.csv"
    "precious_metal_gold.csv"
    "precious_metal_silver.csv"
    "news_breakfast.csv"
)

mkdir -p "$DATA_DIR"

for file in "${FILES[@]}"; do
    echo "Downloading $file..."
    curl -sL "${BASE_URL}/${file}" -o "${DATA_DIR}/${file}"
done

echo "Done! Downloaded ${#FILES[@]} files to ${DATA_DIR}"
