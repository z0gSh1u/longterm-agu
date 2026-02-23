"""
日历事件管理工具 - CLI 入口
"""

from __future__ import annotations

import argparse
import sys

from .storage import (
    add_event,
    query_events,
    remove_event,
    upcoming_events,
    VALID_CATEGORIES,
)


def _format_events(events: list) -> str:
    """格式化事件列表为表格字符串。"""
    if not events:
        return "无事件"

    lines = []
    lines.append(f"{'ID':<6}{'日期':<14}{'分类':<14}{'来源':<14}{'事件'}")
    lines.append("-" * 80)
    for e in events:
        lines.append(f"{e.id:<6}{e.date:<14}{e.category:<14}{e.source:<14}{e.event}")
    lines.append(f"\n共 {len(events)} 条事件")
    return "\n".join(lines)


def cmd_add(args: argparse.Namespace) -> None:
    event = add_event(
        event_date=args.date,
        event=args.event,
        category=args.category,
        source=args.source,
    )
    print(f"已添加事件 (ID={event.id}): [{event.date}] {event.event}")


def cmd_query(args: argparse.Namespace) -> None:
    events = query_events(args.date_from, args.date_to)
    print(_format_events(events))


def cmd_upcoming(args: argparse.Namespace) -> None:
    events = upcoming_events(args.days)
    print(f"未来 {args.days} 天事件:")
    print(_format_events(events))


def cmd_remove(args: argparse.Namespace) -> None:
    if remove_event(args.id):
        print(f"已删除事件 (ID={args.id})")
    else:
        print(f"未找到事件 (ID={args.id})", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="calendar-tool",
        description="日历事件管理工具 - 增删改查金融事件日历",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add 子命令
    add_parser = subparsers.add_parser("add", help="添加事件")
    add_parser.add_argument("--date", required=True, help="事件日期 (YYYY-MM-DD)")
    add_parser.add_argument("--event", required=True, help="事件描述")
    add_parser.add_argument(
        "--category",
        required=True,
        choices=sorted(VALID_CATEGORIES),
        help="事件分类",
    )
    add_parser.add_argument(
        "--source",
        default="manual",
        choices=["manual", "news_extract"],
        help="事件来源 (默认: manual)",
    )

    # query 子命令
    query_parser = subparsers.add_parser("query", help="按日期范围查询事件")
    query_parser.add_argument(
        "--from", dest="date_from", required=True, help="起始日期 (YYYY-MM-DD)"
    )
    query_parser.add_argument(
        "--to", dest="date_to", required=True, help="结束日期 (YYYY-MM-DD)"
    )

    # upcoming 子命令
    upcoming_parser = subparsers.add_parser("upcoming", help="查询未来 N 天事件")
    upcoming_parser.add_argument("--days", type=int, default=14, help="天数 (默认: 14)")

    # remove 子命令
    remove_parser = subparsers.add_parser("remove", help="删除事件")
    remove_parser.add_argument("--id", type=int, required=True, help="事件 ID")

    args = parser.parse_args()

    try:
        if args.command == "add":
            cmd_add(args)
        elif args.command == "query":
            cmd_query(args)
        elif args.command == "upcoming":
            cmd_upcoming(args)
        elif args.command == "remove":
            cmd_remove(args)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
