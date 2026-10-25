# 三千年账本 · Ledger of Empires

用一张资产负债表重读中国金融史：8 个财政-货币内核、24 张决策卡、Python/Excel 情景模拟。

> Every empire keeps books. Every empire goes bankrupt.

## 状态

M1 进行中：前 6 章章节包、6 张卡、3 篇文章、数据管道 v0、Excel 骨架。

## 结构

- `00-总控/`：作战卡、进度表、决策日志、术语表
- `01-章节/`：24 章章节包
- `02-卡片/`：8 内核 × 3 张决策卡
- `03-数据/`：原始数据、清洗数据、出处、字段说明
- `04-模型/`：Excel + Python 模型
- `05-输出/`：文章、工作台、课程、B2B
- `06-亲子/`：8 个故事 + 磁力片游戏
- `07-复盘/`：4 个里程碑复盘
- `_private/`：私有草稿，不进仓库

## 快速开始

```bash
pip install -r requirements.txt
pytest -q
python scripts/validate.py --all
```

## 互动故事

线上：https://justinjchen-cornell.github.io/Ledger-of-Empires/

第 1 章可玩版本：`05-输出/工作台/story.html`。本地预览见 `05-输出/工作台/README.md`。

## 许可

代码 MIT；文字 CC BY-NC-SA 4.0。书籍原文不在本仓库，章节包只含原创摘要和短引文。
