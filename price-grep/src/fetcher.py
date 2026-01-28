"""
数据获取模块 - 从 akshare 获取股指和贵金属数据
"""

import akshare as ak
import pandas as pd


# 目标股票指数：中文符号名 -> 英文文件名
STOCK_INDICES = {
    "上证指数": "sse_composite",
    "沪深300": "csi300",
    "创业板指": "chinext",
    "恒生指数": "hsi",
    "标普500": "sp500",
    "纳斯达克": "nasdaq",
}

# 目标贵金属：中文名 -> 英文文件名
PRECIOUS_METALS = {
    "黄金": "gold",
    "白银": "silver",
}

# 股指列名映射：中文 -> 英文
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

# 贵金属列名映射：中文 -> 英文
PRECIOUS_METAL_COLUMN_MAP = {
    "交易时间": "date",
    "晚盘价": "evening_price",
    "早盘价": "morning_price",
}


def _standardize_columns(df: pd.DataFrame, column_map: dict[str, str]) -> pd.DataFrame:
    """将 DataFrame 的列名从中文转换为英文"""
    # 只重命名存在的列
    rename_map = {k: v for k, v in column_map.items() if k in df.columns}
    return df.rename(columns=rename_map)


def fetch_stock_index(symbol: str) -> pd.DataFrame:
    """
    获取单个股指的历史K线数据

    Args:
        symbol: 股指名称，如 "上证指数"、"沪深300" 等

    Returns:
        标准化列名的 DataFrame，包含 date, code, name, open, close, high, low, amplitude

    Raises:
        Exception: API 调用失败或返回空数据时抛出异常
    """
    print(f"正在获取股指数据: {symbol}")
    df = ak.index_global_hist_em(symbol=symbol)

    if df is None or df.empty:
        raise ValueError(f"获取股指 {symbol} 数据失败：返回数据为空")

    df = _standardize_columns(df, STOCK_INDEX_COLUMN_MAP)
    print(f"  获取到 {len(df)} 条记录")
    return df


def fetch_all_stock_indices() -> dict[str, pd.DataFrame]:
    """
    获取所有目标股指数据

    Returns:
        {symbol: DataFrame} 字典

    Raises:
        Exception: 任意一个股指获取失败时抛出异常
    """
    result = {}
    for symbol in STOCK_INDICES:
        result[symbol] = fetch_stock_index(symbol)
    return result


def fetch_precious_metal(metal: str) -> pd.DataFrame:
    """
    获取单个贵金属的历史价格数据

    Args:
        metal: 贵金属名称，"黄金" 或 "白银"

    Returns:
        标准化列名的 DataFrame，包含 date, evening_price, morning_price

    Raises:
        Exception: API 调用失败或返回空数据时抛出异常
    """
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
    """
    获取所有目标贵金属数据

    Returns:
        {metal: DataFrame} 字典

    Raises:
        Exception: 任意一个贵金属获取失败时抛出异常
    """
    result = {}
    for metal in PRECIOUS_METALS:
        result[metal] = fetch_precious_metal(metal)
    return result
