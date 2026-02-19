"""
数据存储模块 - CSV 文件的读写和增量更新
"""

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent.parent.parent / "data"


def get_data_path(category: str, name: str) -> Path:
    return DATA_DIR / f"{category}_{name}.csv"


def save_full_history(df: pd.DataFrame, category: str, name: str) -> None:
    file_path = get_data_path(category, name)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"  已保存到 {file_path} ({len(df)} 条记录)")


def load_existing_data(category: str, name: str) -> pd.DataFrame | None:
    file_path = get_data_path(category, name)

    if not file_path.exists():
        return None

    return pd.read_csv(file_path, encoding="utf-8-sig")


def append_daily_data(df: pd.DataFrame, category: str, name: str) -> int:
    file_path = get_data_path(category, name)
    existing_df = load_existing_data(category, name)

    if existing_df is None:
        save_full_history(df, category, name)
        return len(df)

    df["date"] = df["date"].astype(str)
    existing_df["date"] = existing_df["date"].astype(str)

    existing_dates = set(existing_df["date"].tolist())
    new_rows = df[~df["date"].isin(existing_dates)]

    if new_rows.empty:
        print(f"  {name}: 无新数据")
        return 0

    new_rows.to_csv(
        file_path, mode="a", header=False, index=False, encoding="utf-8-sig"
    )
    print(f"  {name}: 新增 {len(new_rows)} 条记录")

    return len(new_rows)
