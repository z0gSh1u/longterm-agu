"""
Price grep package - 金融数据获取工具
"""

from .fetcher import (
    PRECIOUS_METALS,
    STOCK_INDICES,
    fetch_precious_metal,
    fetch_stock_index,
)
from .storage import append_daily_data, save_full_history

__all__ = [
    "STOCK_INDICES",
    "PRECIOUS_METALS",
    "fetch_stock_index",
    "fetch_precious_metal",
    "save_full_history",
    "append_daily_data",
]
