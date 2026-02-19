"""
数据获取模块 - 从 akshare 获取股指和贵金属数据
"""

import akshare as ak
import pandas as pd


STOCK_INDICES = {
    "上证指数": "sse_composite",
    "沪深300": "csi300",
    "创业板指": "chinext",
    "恒生指数": "hsi",
    "标普500": "sp500",
    "纳斯达克": "nasdaq",
}

PRECIOUS_METALS = {
    "黄金": "gold",
    "白银": "silver",
}

STOCK_INDEX_COLUMN_MAP = {
    "日期": "date",
    "代码": "code",
    "名称": "name",
    "今开": "open",
    "最新价": "close",
    "最高": "high",
    "最低": "low",
    "振幅": "amplitude",
}

PRECIOUS_METAL_COLUMN_MAP = {
    "交易时间": "date",
    "晚盘价": "evening_price",
    "早盘价": "morning_price",
}


def _standardize_columns(df: pd.DataFrame, column_map: dict[str, str]) -> pd.DataFrame:
    rename_map = {k: v for k, v in column_map.items() if k in df.columns}
    return df.rename(columns=rename_map)


def fetch_stock_index(symbol: str) -> pd.DataFrame:
    print(f"正在获取股指数据: {symbol}")
    df = ak.index_global_hist_em(symbol=symbol)

    if df is None or df.empty:
        raise ValueError(f"获取股指 {symbol} 数据失败：返回数据为空")

    df = _standardize_columns(df, STOCK_INDEX_COLUMN_MAP)
    print(f"  获取到 {len(df)} 条记录")
    return df


def fetch_all_stock_indices() -> dict[str, pd.DataFrame]:
    result = {}
    for symbol in STOCK_INDICES:
        result[symbol] = fetch_stock_index(symbol)
    return result


def fetch_precious_metal(metal: str) -> pd.DataFrame:
    print(f"正在获取贵金属数据: {metal}")

    if metal == "黄金":
        df = ak.spot_golden_benchmark_sge()
    elif metal == "白银":
        df = ak.spot_silver_benchmark_sge()
    else:
        raise ValueError(f"不支持的贵金属类型: {metal}")

    if df is None or df.empty:
        raise ValueError(f"获取贵金属 {metal} 数据失败：返回数据为空")

    df = _standardize_columns(df, PRECIOUS_METAL_COLUMN_MAP)
    print(f"  获取到 {len(df)} 条记录")
    return df


def fetch_all_precious_metals() -> dict[str, pd.DataFrame]:
    result = {}
    for metal in PRECIOUS_METALS:
        result[metal] = fetch_precious_metal(metal)
    return result
