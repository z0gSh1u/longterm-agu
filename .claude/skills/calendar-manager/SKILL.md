---
name: calendar-manager
description: Manage the investment event calendar. Use when the user mentions calendar events, asks about upcoming events, wants to add/remove events, or when performing investment analysis that needs to check future events. Also use when processing news to extract future events.
compatibility: Requires uv and the calendar-tool entry point defined in pyproject.toml
---

# 日历管理器

## 日历工具 CLI

所有日历操作必须通过 CLI 工具完成。**严禁直接编辑 `data/calendar.csv`。**

### 添加事件

```bash
uv run calendar-tool add --date YYYY-MM-DD --event "事件描述" --category <category>
```

### 按日期范围查询事件

```bash
uv run calendar-tool query --from YYYY-MM-DD --to YYYY-MM-DD
```

### 查看即将发生的事件（未来 N 天）

```bash
uv run calendar-tool upcoming --days 14
```

### 删除事件

```bash
uv run calendar-tool remove --id <event_id>
```

## 事件分类

- `macro` — 宏观经济数据发布（CPI、GDP、PMI）、央行利率决议、货币政策会议
- `policy` — 政策法规实施、监管动态、政府工作报告
- `earnings` — 财报季、重要上市公司业绩公告
- `geopolitical` — 国际关系、贸易谈判、制裁、地缘冲突
- `market` — IPO、指数调整、期货交割日、股指期权到期
- `other` — 其他不属于以上分类的事件

## 从新闻中提取事件

当用户要求从新闻中提取当天或未来事件，或在分析过程中判断有必要主动提取时：

1. 使用 Read 工具读取目标日期的 `data/news_breakfast.csv`
2. 逐条分析新闻摘要，识别文中提及的 **当天事件** 和 **未来事件**，重点关注：
   - 已排期的会议或发布会（如"下周将召开……"、"定于X月X日……"）
   - 数据发布日期（如"将于X日公布……"、"预计X月发布……"）
   - 政策实施日期（如"自X月X日起实施……"）
   - 财报公告或财务截止日期
3. 对每个识别出的未来事件：
   - 先运行 `uv run calendar-tool query --from <date> --to <date>` 检查是否已存在
   - 若无重复，运行 `uv run calendar-tool add --date <date> --event "<描述>" --category <category> --source news_extract`
4. 向用户汇报提取并添加了哪些事件

## 重要规则

- 始终通过 CLI 工具操作，严禁直接编辑 CSV
- 从新闻添加事件时，必须设置 `--source news_extract`
- 用户手动请求添加事件时，使用默认来源 `--source manual`
- 添加前通过 `query` 检查重复，避免冗余条目
- 日期格式必须为 YYYY-MM-DD

另外，不是每一条新闻都包含有价值的、需要被持久化到日历中的当天或未来事件，需要进行判断和筛选。例如：

- 「2026-01-05,比亚迪2025年全年累计销量超460万辆，同比增长7.73%」
  这条新闻的事件与 2026 年 1 月 5 日并没有直接关联，没有必要添加到日历中
- 「2026-02-11,多家机器人企业成为2026年春晚合作伙伴，具身智能机器人将组团登上春晚舞台。」
  这条新闻提到的事件是「2026年春晚」，且具身智能是重要的投资板块，因此可以网络搜索查证 2026 年春晚的具体日期后，将此事件添加到日历中。
