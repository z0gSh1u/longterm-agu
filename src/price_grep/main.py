"""
命令行入口 - 自动增量补齐
"""

import argparse
import sys

from .fetcher import (
    PRECIOUS_METALS,
    STOCK_INDICES,
    fetch_precious_metal,
    fetch_stock_index,
)
from .storage import append_daily_data, get_existing_dates, log_error


def run() -> None:
    print("=" * 50)
    print("运行模式: 自动增量补齐")
    print("=" * 50)

    total_new_records = 0
    total_existing_records = 0

    print("\n[1/2] 处理股票指数数据...")
    for symbol, file_id in STOCK_INDICES.items():
        existing_dates = get_existing_dates("stock_index", file_id)
        total_existing_records += len(existing_dates)

        df = fetch_stock_index(symbol)
        new_count = append_daily_data(df, "stock_index", file_id)
        total_new_records += new_count

    print("\n[2/2] 处理贵金属数据...")
    for metal, file_id in PRECIOUS_METALS.items():
        existing_dates = get_existing_dates("precious_metal", file_id)
        total_existing_records += len(existing_dates)

        df = fetch_precious_metal(metal)
        new_count = append_daily_data(df, "precious_metal", file_id)
        total_new_records += new_count

    print("\n" + "=" * 50)
    print(f"执行完成! 存量: {total_existing_records} 条, 新增: {total_new_records} 条")
    print("=" * 50)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="price-grep",
        description="金融数据获取工具 - 股指和贵金属数据",
    )

    args = parser.parse_args([])

    try:
        run()
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
