# Skill: calendar-manager

Use when the user mentions calendar events, asks about upcoming events, wants to add/remove events, or when performing investment analysis that needs to check future events. Also use when processing news to extract future events.

## Calendar Tool CLI

All calendar operations MUST go through the CLI tool. NEVER directly edit `data/calendar.csv`.

### Add an event

```bash
uv run calendar-tool add --date YYYY-MM-DD --event "事件描述" --category <category>
```

### Query events by date range

```bash
uv run calendar-tool query --from YYYY-MM-DD --to YYYY-MM-DD
```

### View upcoming events (next N days)

```bash
uv run calendar-tool upcoming --days 14
```

### Remove an event

```bash
uv run calendar-tool remove --id <event_id>
```

## Event Categories

- `macro` — 宏观经济数据发布（CPI、GDP、PMI）、央行利率决议、货币政策会议
- `policy` — 政策法规实施、监管动态、政府工作报告
- `earnings` — 财报季、重要上市公司业绩公告
- `geopolitical` — 国际关系、贸易谈判、制裁、地缘冲突
- `market` — IPO、指数调整、期货交割日、股指期权到期
- `other` — 其他不属于以上分类的事件

## Extracting Events from News

When asked to extract future events from news, or when it is appropriate to proactively do so during analysis:

1. Read `data/news_breakfast.csv` for the target date(s) using the Read tool
2. Analyze each news summary to identify **future events** mentioned in the text — look for:
   - Scheduled meetings or conferences (e.g., "下周将召开...", "定于X月X日...")
   - Data release dates (e.g., "将于X日公布...", "预计X月发布...")
   - Policy implementation dates (e.g., "自X月X日起实施...")
   - Earnings announcements or financial deadlines
3. For each identified future event:
   - First run `uv run calendar-tool query --from <date> --to <date>` to check if it already exists
   - If not duplicate, run `uv run calendar-tool add --date <date> --event "<description>" --category <category> --source news_extract`
4. Report to the user what events were extracted and added

## Important Rules

- Always use the CLI tool, never edit the CSV directly
- When adding events from news, always set `--source news_extract`
- When the user manually requests adding an event, use default `--source manual`
- Before adding, check for duplicates via `query` to avoid redundant entries
- Dates must be in YYYY-MM-DD format
