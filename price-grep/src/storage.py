"""
数据存储模块 - CSV 文件的读写和增量更新
"""

from pathlib import Path

import pandas as pd


# 数据目录路径（相对于 price-grep 根目录）
DATA_DIR = Path(__file__).parent.parent / "data"


def get_data_path(category: str, name: str) -> Path:
    """
    获取数据文件路径

    Args:
        category: 数据类别，如 "stock_index" 或 "precious_metal"
        name: 具体名称，如 "上证指数" 或 "黄金"

    Returns:
        文件路径: data/{category}_{name}.csv
    """
    return DATA_DIR / f"{category}_{name}.csv"


def save_full_history(df: pd.DataFrame, category: str, name: str) -> None:
    """
    全量保存历史数据到 CSV

    Args:
        df: 要保存的 DataFrame
        category: 数据类别
        name: 具体名称
    """
    file_path = get_data_path(category, name)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"  已保存到 {file_path} ({len(df)} 条记录)")


def load_existing_data(category: str, name: str) -> pd.DataFrame | None:
    """
    加载现有 CSV 数据

    Args:
        category: 数据类别
        name: 具体名称

    Returns:
        DataFrame 或 None（文件不存在时）
    """
    file_path = get_data_path(category, name)

    if not file_path.exists():
        return None

    return pd.read_csv(file_path, encoding="utf-8-sig")


def append_daily_data(df: pd.DataFrame, category: str, name: str) -> int:
    """
    追加新数据到现有 CSV，基于 date 列去重

    Args:
        df: 新获取的完整 DataFrame
        category: 数据类别
        name: 具体名称

    Returns:
        新增行数
    """
    file_path = get_data_path(category, name)
    existing_df = load_existing_data(category, name)

    if existing_df is None:
        # 文件不存在，直接保存全量数据
        save_full_history(df, category, name)
        return len(df)

    # 确保 date 列为字符串类型以便比较
    df["date"] = df["date"].astype(str)
    existing_df["date"] = existing_df["date"].astype(str)

    # 找出新数据中不在现有数据的日期
    existing_dates = set(existing_df["date"].tolist())
    new_rows = df[~df["date"].isin(existing_dates)]

    if new_rows.empty:
        print(f"  {name}: 无新数据")
        return 0

    # 追加新行到 CSV
    new_rows.to_csv(
        file_path, mode="a", header=False, index=False, encoding="utf-8-sig"
    )
    print(f"  {name}: 新增 {len(new_rows)} 条记录")

    return len(new_rows)
