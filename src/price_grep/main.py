"""
命令行入口 - 支持 full 和 daily 两种运行模式
"""

import argparse
import sys

from .fetcher import (
    PRECIOUS_METALS,
    STOCK_INDICES,
    fetch_precious_metal,
    fetch_stock_index,
)
from .storage import append_daily_data, save_full_history


def run_full_mode() -> None:
    print("=" * 50)
    print("运行模式: FULL (全量获取)")
    print("=" * 50)

    print("\n[1/2] 获取股票指数数据...")
    for symbol, file_id in STOCK_INDICES.items():
        df = fetch_stock_index(symbol)
        save_full_history(df, "stock_index", file_id)

    print("\n[2/2] 获取贵金属数据...")
    for metal, file_id in PRECIOUS_METALS.items():
        df = fetch_precious_metal(metal)
        save_full_history(df, "precious_metal", file_id)

    print("\n" + "=" * 50)
    print("全量数据获取完成!")
    print("=" * 50)


def run_daily_mode() -> None:
    print("=" * 50)
    print("运行模式: DAILY (增量更新)")
    print("=" * 50)

    total_new_records = 0

    print("\n[1/2] 更新股票指数数据...")
    for symbol, file_id in STOCK_INDICES.items():
        df = fetch_stock_index(symbol)
        new_count = append_daily_data(df, "stock_index", file_id)
        total_new_records += new_count

    print("\n[2/2] 更新贵金属数据...")
    for metal, file_id in PRECIOUS_METALS.items():
        df = fetch_precious_metal(metal)
        new_count = append_daily_data(df, "precious_metal", file_id)
        total_new_records += new_count

    print("\n" + "=" * 50)
    print(f"每日更新完成! 共新增 {total_new_records} 条记录")
    print("=" * 50)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="price-grep",
        description="金融数据获取工具 - 支持股指和贵金属数据",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "daily"],
        required=True,
        help="运行模式: full=全量获取, daily=增量更新",
    )

    args = parser.parse_args()

    try:
        if args.mode == "full":
            run_full_mode()
        elif args.mode == "daily":
            run_daily_mode()
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
