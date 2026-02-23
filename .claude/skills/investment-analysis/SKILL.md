---
name: investment-analysis
description: Analyze Chinese and global financial markets using local price data, news, and calendar events. Use when the user asks about market trends, investment analysis, stock indices, precious metals, or requests an investment report. Also use when the user mentions specific indices (上证, 沪深300, 创业板, 恒生, 标普500, 纳斯达克) or metals (黄金, 白银, 沪金, 沪银).
compatibility: Requires uv and the calendar-tool entry point defined in pyproject.toml
---

# 投资分析

## 可用数据

所有数据位于 `data/` 目录：

### 股票指数（日线 OHLC）

| 文件                                 | 指数     | 字段                                                |
| ------------------------------------ | -------- | --------------------------------------------------- |
| `data/stock_index_sse_composite.csv` | 上证指数 | date, code, name, open, close, high, low, amplitude |
| `data/stock_index_csi300.csv`        | 沪深300  | 同上                                                |
| `data/stock_index_chinext.csv`       | 创业板指 | 同上                                                |
| `data/stock_index_hsi.csv`           | 恒生指数 | 同上                                                |
| `data/stock_index_sp500.csv`         | 标普500  | 同上                                                |
| `data/stock_index_nasdaq.csv`        | 纳斯达克 | 同上                                                |

涨跌判断：收盘 > 开盘 = 涨，收盘 < 开盘 = 跌

### 贵金属（日线，沪金单位：元/克；沪银单位：元/千克）

| 文件                             | 品种 | 字段                               |
| -------------------------------- | ---- | ---------------------------------- |
| `data/precious_metal_gold.csv`   | 沪金 | date, evening_price, morning_price |
| `data/precious_metal_silver.csv` | 沪银 | date, evening_price, morning_price |

### 财经新闻

| 文件                      | 字段                              |
| ------------------------- | --------------------------------- |
| `data/news_breakfast.csv` | date, summary, source_url, source |

来自东方财富的每日财经早餐摘要，经 AI 处理。

### 日历事件

| 文件                | 字段                                          |
| ------------------- | --------------------------------------------- |
| `data/calendar.csv` | id, date, event, category, source, added_date |

通过 `uv run calendar-tool` CLI 管理，详见 calendar-manager skill。

## 分析流程

执行投资分析时，**按以下顺序**逐步操作：

### 第一步：加载数据

使用 Read 工具读取相关 CSV 文件。近期分析读取每个文件末尾 200 行（使用 `offset` 参数）；长期趋势分析适当多读。

也可以使用 Grep 工具带着日期来读取 CSV 文件，快速定位到所需数据行。

始终检查每个文件中的最新日期，若数据未更新到今天，须向用户说明数据滞后情况。

### 第二步：查看日历

```bash
uv run calendar-tool upcoming --days 14
```

在开始分析前，先浏览所有近期事件及其潜在市场影响。

### 第三步：技术面分析

基于 OHLC 数据分析：

- **趋势方向**：对比近 5/10/20/60 个交易日，市场处于上升、下降还是横盘？
- **支撑与压力**：识别近期高点低点、关键整数关口
- **振幅/波动率**：波动率是扩张还是收窄？释放什么信号？
- **价格位置**：当前价格在近期区间中处于什么位置？靠近近期高点（压力区）还是低点（支撑区）？

在脑中对数据做如下计算：

- MA5 = 最近 5 根收盘均值
- MA10 = 最近 10 根收盘均值
- MA20 = 最近 20 根收盘均值

判断短期均线是否在长期均线上方（金叉 / 死叉信号）。

### 第四步：消息面分析

读取 `data/news_breakfast.csv` 近 7～14 天的条目，识别：

- 重大政策变化（财政刺激、货币宽松/收紧）
- 行业动态（监管整治、行业扶持）
- 国际贸易 / 地缘政治事件（关税、制裁、峰会）
- 监管行动（IPO 暂停、资本市场规则调整）

对每条关键新闻，判断：对哪些市场利多/利空/中性？

### 第五步：跨市场联动

比较各市场趋势：

- **美股→A股传导**：标普500/纳斯达克走势通常领先 A 股（上证/沪深300/创业板）情绪约 1 个交易日
- **港股桥梁**：恒生指数同时反映美股隔夜走势和中国基本面，是有效的领先指标
- **黄金 vs 股票**：黄金上涨而股票下跌 = 避险信号；反向关系为常态，但并非绝对
- **白银**：工业需求属性强于黄金；白银上涨而黄金稳定 = 经济增长乐观信号

### 第六步：前瞻研判

结合日历事件与历史规律：

- 哪些近期事件可能引发市场波动？（参考第二步的日历查询结果）
- 市场历史上如何应对类似事件类型？
- 季节性规律：春节行情（涨/节后回调）、年末窗口期、季度再平衡
- 政策周期：目前处于货币/财政周期的哪个阶段？宽松末期需谨慎，刺激初期是机会

对不确定性要明确表达，如："历史上 X 倾向于 Y，但当前背景 Z 可能有所不同。"

### 第七步：输出

**对话式分析**：直接回答用户的具体问题，引用数据中的具体日期、价格和涨跌幅，不要堆砌无关内容。

**报告生成**：将 Markdown 报告写入 `docs/reports/YYYY-MM-DD-<type>.md`，类型使用 `daily` 或 `weekly`，格式参见下方模板。

## 报告模板

保存至：`docs/reports/YYYY-MM-DD-<type>.md`

    # 投资分析报告 — YYYY-MM-DD

    ## 市场概览

    （各市场最近交易日的表现。用表格呈现：市场名称 | 收盘价 | 涨跌幅 | 振幅）

    ## 技术面分析

    （对各主要指数的趋势方向、支撑压力位、波动率变化分析。引用具体价格和日期。）

    ## 消息面解读

    （近期重要新闻摘要及其对市场的影响分析。每条新闻标注日期，评估影响：利多/利空/中性。）

    ## 跨市场联动

    （全球市场相关性分析：美股传导、港股桥梁作用、贵金属避险信号。）

    ## 未来事件与展望

    （日历中的近期事件列表 + 基于分析的前瞻研判。每个事件标注日期和潜在影响方向。）

    ## 风险提示

    （当前需关注的关键风险因素。）

    ---
    *分析仅供参考，不构成投资建议。*

## 重要规则

- 始终引用数据中的具体日期和数字，严禁捏造数据
- 对趋势不确定时，明确说明——不要强行将随机波动纳入叙事
- 所有输出必须包含免责声明：分析仅供参考，不构成投资建议
- 日历操作使用 calendar-manager skill（通过 `uv run calendar-tool`）
- 数据可能未更新到今天——始终检查 CSV 中的最新日期，并向用户说明数据滞后情况
- 长期分析（月/年）多读行数；日/周分析读取末尾 60～200 行即可
