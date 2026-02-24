# Calendar 边界重设计实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 重新划分 `calendar_tool` 和 `news_breakfast` 的职责边界，使 Calendar 只存储"有明确日期、已被官方公告的确定性事件"，彻底去除从 news 自动提取事件这条数据通道。

**Architecture:** Calendar 定位为用户主动维护的宏观日历（Fed 会议、数据公布日、财报日等），去除 `news_extract` source；news_breakfast 继续作为回溯性新闻摘要。两者在投资分析时并列使用，无数据流动。

**Tech Stack:** Python, pandas, argparse, Markdown (SKILL.md)

---

## 背景与设计决策

### 问题
当前设计允许 `source=news_extract`，鼓励 AI 从 news_breakfast 读取新闻并提取未来事件写入 Calendar。这带来两个问题：
1. **语义重叠**：news_breakfast 里已有未来事件的文字描述，Calendar 重复存储一遍
2. **可信度稀释**：新闻里的未来事件往往是"预期/报道"而非"官方排期"，混入 Calendar 降低其权威性

### 决策
- **Calendar = 确定性事件**：只存有明确日期、官方公告的排期（如美联储会议日历、CPI 公布日）
- **去除 `news_extract` source**：`VALID_SOURCES` 只保留 `"manual"`，CLI 的 `--source` 参数随之简化
- **calendar-manager skill 更新**：移除"从新闻提取事件"的工作流，改为引导用户手动维护权威日历
- **investment-analysis skill 更新**：更新对两者关系的描述，强调 Calendar 的确定性定位

---

## Task 1: 更新 storage.py — 移除 news_extract source

**Files:**
- Modify: `src/calendar_tool/storage.py:19`

**Step 1: 修改 `VALID_SOURCES`**

将 `storage.py` 第 19 行：
```python
VALID_SOURCES = {"manual", "news_extract"}
```
改为：
```python
VALID_SOURCES = {"manual"}
```

**Step 2: 验证**

```bash
uv run python -c "from src.calendar_tool.storage import VALID_SOURCES; print(VALID_SOURCES)"
```
预期输出：`{'manual'}`

**Step 3: 运行现有测试（如有）**

```bash
uv run pytest tests/ -v 2>/dev/null || echo "no tests"
```

**Step 4: Commit**

```bash
git add src/calendar_tool/storage.py
git commit -m "refactor: remove news_extract source from calendar tool"
```

---

## Task 2: 更新 main.py — 简化 --source 参数

**Files:**
- Modify: `src/calendar_tool/main.py:83-87`

**Step 1: 修改 `add` 子命令的 `--source` 参数**

将 `main.py` 中 `--source` 的 choices 从 `["manual", "news_extract"]` 改为只有 `["manual"]`，并移除 help 文本中对 `news_extract` 的提及：

```python
add_parser.add_argument(
    "--source",
    default="manual",
    choices=["manual"],
    help="事件来源 (默认: manual)",
)
```

实际上，`--source` 现在只有一个选项，可以考虑完全隐藏这个参数（保留但设为内部参数）。保留它以便未来扩展，但不在 help 中显式列出选项。

**Step 2: 验证 CLI 帮助**

```bash
uv run calendar-tool add --help
```
预期：`--source` 不再提示 `news_extract` 选项

**Step 3: 验证拒绝无效 source**

```bash
uv run calendar-tool add --date 2026-03-01 --event "test" --category macro --source news_extract
```
预期：报错退出，提示无效来源

**Step 4: Commit**

```bash
git add src/calendar_tool/main.py
git commit -m "refactor: simplify --source option, only manual allowed"
```

---

## Task 3: 更新 calendar-manager/SKILL.md

**Files:**
- Modify: `.claude/skills/calendar-manager/SKILL.md`

**Step 1: 重写 SKILL.md**

核心改动：
1. 移除"从新闻中提取事件"整个章节（原 L46–63）
2. 更新 `--source` 用法说明，去除 `news_extract`
3. 在"重要规则"中明确 Calendar 的定位：只存官方排期的确定性事件
4. 新增"Calendar 定位"说明段落，举例说明哪些事件适合/不适合入库

新的 SKILL.md 内容：

```markdown
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
```

**Step 2: 验证文件内容正确**

用 Read 工具确认文件保存正常。

**Step 3: Commit**

```bash
git add .claude/skills/calendar-manager/SKILL.md
git commit -m "docs: redefine calendar as deterministic-only, remove news_extract workflow"
```

---

## Task 4: 更新 investment-analysis/SKILL.md

**Files:**
- Modify: `.claude/skills/investment-analysis/SKILL.md`

**Step 1: 更新数据说明中的 Calendar 描述**

在"日历事件"数据表下方，添加一行说明 Calendar 的定位：

原文（L 约 50）：
```markdown
| `data/calendar.csv` | id, date, event, category, source, added_date |

通过 `uv run calendar-tool` CLI 管理，详见 calendar-manager skill。
```

改为：
```markdown
| `data/calendar.csv` | id, date, event, category, source, added_date |

通过 `uv run calendar-tool` CLI 管理，详见 calendar-manager skill。
**只包含确定性事件**（官方公告的排期），不含从新闻推断的预期性事件。
```

**Step 2: 更新第四步消息面分析说明**

在第四步末尾补充一句，明确 news_breakfast 和 Calendar 的职责分工：

原文（第四步末尾）：
```markdown
对每条关键新闻，判断：对哪些市场利多/利空/中性？
```

改为：
```markdown
对每条关键新闻，判断：对哪些市场利多/利空/中性？

> 注：news_breakfast 包含模糊预期性的未来事件描述；Calendar 只含官方排期的确定性事件。两者互补，分析时区别对待。
```

**Step 3: Commit**

```bash
git add .claude/skills/investment-analysis/SKILL.md
git commit -m "docs: clarify calendar vs news_breakfast boundary in investment-analysis skill"
```

---

## Task 5: 更新 README.md

**Files:**
- Modify: `README.md`

**Step 1: 更新 calendar-tool 章节说明**

在 README 的 `calendar-tool` 段落中，`--source` 示例部分不再展示 `news_extract`，并在分类说明后补充 Calendar 定位说明：

找到：
```markdown
事件分类：`macro`（宏观）、`policy`（政策）、`earnings`（财报）、`geopolitical`（地缘）、`market`（市场）、`other`
```

改为：
```markdown
事件分类：`macro`（宏观）、`policy`（政策）、`earnings`（财报）、`geopolitical`（地缘）、`market`（市场）、`other`

Calendar 只存储**确定性事件**（官方公告的排期）。新闻中的预期性事件请参阅 `news_breakfast`。
```

**Step 2: 更新 Skills 说明**

将原来提到"从新闻提取事件"的 skill 示例（如 `/calendar-management 从近三天的新闻中提取有明确日期的事件`）移除。

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: update README to reflect calendar deterministic-only policy"
```

---

## 验证完整性

所有 Task 完成后，运行：

```bash
# 确认 news_extract 从代码中彻底消失
grep -r "news_extract" src/ .claude/ README.md
```

预期：无任何匹配（`news_extract` 只应出现在本计划文档中）。
