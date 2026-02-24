---
name: calendar-manager
description: Manage the investment event calendar. Use when the user mentions calendar events, asks about upcoming events, wants to add/remove events, or when performing investment analysis that needs to check future events.
compatibility: Requires uv and the calendar-tool entry point defined in pyproject.toml
---

# 日历管理器

## Calendar 定位

**Calendar 只存储确定性事件**：有明确日期、已被官方公告或权威来源确认的排期事件。

适合入库的事件：
- 美联储 FOMC 会议（已公布全年日历）
- 中国 CPI/PPI/PMI 等宏观数据发布日（统计局公告）
- 上市公司财报截止日/业绩公告日（交易所公告）
- 重要政策实施日（已颁布的法规生效日期）

**不适合**入库的事件：
- 新闻中提及的"预计"/"可能"/"将于"等模糊预期
- 从财经早餐中读到的、尚未官方确认的未来事件
- 已经发生的历史事件（那是 news_breakfast 的领域）

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

## 重要规则

- 始终通过 CLI 工具操作，严禁直接编辑 CSV
- 只添加**确定性**事件：必须有明确日期且来源权威（官方公告、交易所披露等）
- 用户手动请求添加事件时，使用默认来源 `--source manual`
- 添加前通过 `query` 检查重复，避免冗余条目
- 日期格式必须为 YYYY-MM-DD
- **不要**将 news_breakfast 中读到的未来事件写入 Calendar——那些事件属于新闻报道层面，不具备 Calendar 要求的确定性
