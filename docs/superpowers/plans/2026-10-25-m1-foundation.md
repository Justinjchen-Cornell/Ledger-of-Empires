# M1 实现计划 — 三千年账本 · Ledger of Empires

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 交付 M1：可运行的章节学习流水线 + 前 6 章章节包/卡片 + 数据管道 v0 + Excel 骨架 + 3 篇文章。

**Architecture:** 内容与代码双轨。代码用 pytest TDD；内容用 `scripts/validate.py` + 用户签字验收。书籍原文只进 `_private/`，仓库只存原创摘要和短引文。

**Tech Stack:** Python 3.11+、pandas、openpyxl、pytest、requests、Markdown、Git。

## Global Constraints

- 中文为主，技术术语保留英文。
- 不提交完整书籍文本；每条引文 < 200 字，带原文行号。
- `_private/` 已 gitignored，书籍清洗稿和章节原文只放这里。
- 每个数据点必须有 `source_id` + `evidence_grade`。
- 每章、每卡、每篇文章必须通过 `python scripts/validate.py`。
- 每个 Task 结束必须 commit。
- 不写占位符；内容任务由执行者按模板生成，但结构和验收标准固定。

## Deviations from Spec

1. 测试统一放根 `tests/`，不分散到 `04-模型/python/tests/`，避免两套测试目录。
2. 书籍清洗稿放 `_private/books/`，不进仓库；仓库只放章节摘要包。
3. 本计划只覆盖 M1（ch1-6）；M2-M4 在 M1 复盘后另写计划。

## File Structure

下表是目录级责任；每个 Task 的 Files 块给出精确路径。

| 路径 | 责任 |
|---|---|
| `README.md` | 项目说明、状态、快速开始 |
| `LICENSE` / `LICENSE-CONTENT` | 代码 MIT / 文字 CC BY-NC-SA 4.0 |
| `requirements.txt` / `pytest.ini` / `conftest.py` | Python 依赖、测试配置、路径注入 |
| `00-总控/作战卡.md` | 目标、范围、节奏、里程碑 |
| `00-总控/进度表.md` | 24 章状态 |
| `00-总控/决策日志.md` | 设计决策记录 |
| `00-总控/术语表.md` | 8 内核 + 关键术语 |
| `scripts/clean_book2.py` | 清洗书 2 的 epub 残留 |
| `scripts/split_chapters.py` | 按章切分两本书到 `_private/books/` |
| `scripts/validate.py` | 章节包 / 卡片 / 文章校验 |
| `scripts/fetch_modern.py` | 拉取 World Bank 现代数据（M1 可选） |
| `templates/chapter.md` | 章节包模板 |
| `templates/card.md` | 决策卡模板 |
| `templates/article.md` | 文章模板 |
| `01-章节/书1-.../ch01-ch06.md` | 前 6 章章节包 |
| `02-卡片/K01-K04/...` | 前 6 章对应的 6 张卡 |
| `03-数据/processed/*.csv` | 5 张数据表 |
| `03-数据/sources.md` | 数据出处登记 |
| `03-数据/data-dictionary.md` | 字段说明 |
| `04-模型/python/data_pipeline.py` | 数据读取 / 校验 |
| `04-模型/python/build_excel.py` | 生成 Excel 骨架 |
| `04-模型/excel/王朝资产负债表.xlsx` | Excel 骨架 |
| `05-输出/文章/01-03.md` | 前 3 篇文章 |
| `07-复盘/里程碑-06.md` | M1 复盘 |
| `tests/` | pytest 测试 |

---

### Task 0: 仓库骨架与治理文件

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `LICENSE-CONTENT`
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create: `conftest.py`
- Create: `00-总控/作战卡.md`
- Create: `00-总控/进度表.md`
- Create: `00-总控/决策日志.md`
- Create: `00-总控/术语表.md`
- Test: `tests/test_repo_skeleton.py`

**Interfaces:**
- Consumes: 无。
- Produces: 后续所有 Task 依赖的目录和治理文件。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_repo_skeleton.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_required_files_exist():
    required = [
        "README.md", "LICENSE", "LICENSE-CONTENT", "requirements.txt", "pytest.ini", "conftest.py",
        "00-总控/作战卡.md", "00-总控/进度表.md", "00-总控/决策日志.md", "00-总控/术语表.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel

def test_progress_table_has_24_chapters():
    text = (ROOT / "00-总控/进度表.md").read_text(encoding="utf-8")
    rows = [line for line in text.splitlines() if line.startswith(("| 书1", "| 书2"))]
    assert len(rows) == 24

def test_glossary_has_all_kernels():
    text = (ROOT / "00-总控/术语表.md").read_text(encoding="utf-8")
    for i in range(1, 9):
        assert f"K{i:02d}" in text
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `pytest tests/test_repo_skeleton.py -q`
Expected: FAIL，提示文件不存在。

- [ ] **Step 3: 创建文件**

`README.md`:

````markdown
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

## 许可

代码 MIT；文字 CC BY-NC-SA 4.0。书籍原文不在本仓库，章节包只含原创摘要和短引文。
````

`LICENSE`：标准 MIT 文本，版权人 `Justin Chen`，年份 `2026`。

`LICENSE-CONTENT`：CC BY-NC-SA 4.0 的简短声明：

```
Copyright (c) 2026 Justin Chen

本仓库中的文字内容（章节包、卡片、文章、课程大纲）采用
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
(CC BY-NC-SA 4.0) 许可。
https://creativecommons.org/licenses/by-nc-sa/4.0/
```

`requirements.txt`:

```
pandas>=2.0
openpyxl>=3.1
pytest>=8.0
requests>=2.31
```

`pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts = -q
```

`conftest.py`:

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
```

`00-总控/作战卡.md`:

```markdown
# 作战卡

## 一句话

用《中国是部金融史》1+2 做一次“学习 + 产出”：24 章 → 24 卡 → 12 篇 → 3 讲 → 8 个亲子故事。

## 数字

- 24 章：书1 12 章 + 书2 12 章
- 8 内核 × 3 卡 = 24 张卡
- 12 篇文章（每 2 章 1 篇）
- 3 讲小课（90min/讲）
- 8 个亲子故事 + 8 张规则卡
- 4 个里程碑：ch6 / ch12 / ch18 / ch24

## 节奏

- 每天至少 1 章；用户说“继续”才进入下一章。
- 每章 35-50 分钟：三幕故事 10-12 + 五层追问 10-15 + 建模 10-15 + 卡片 5。
- 最小可行日：10min 故事 + 1 个决策 + 1 句日志，不做卡。

## 规则

- 不提交完整书籍文本；引文 < 200 字 + 行号。
- 每卡必须有：反事实、失效条件 ≥3、我的异议。
- 公开内容只谈历史机制，不做当代政策判断。
- 先做资产，再做变现。
```

`00-总控/进度表.md`: 24 行表格，状态 `pending`，列：书、章、标题、内核、状态、卡片、文章。标题用两本书的 24 章标题。

`00-总控/决策日志.md`:

```markdown
# 决策日志

## 2026-10-25

- 项目范围：C（全量 + 变现），24 章 + 12 篇 + 3 讲 + B2B + 8 个亲子故事。
- 学习方式：A（三幕说书 + 决策点互动），用户不逐字读原文。
- 节奏：D（每天至少 1 章，用户说“继续”才推进）。
- 模型：C（Excel 王朝资产负债表 + Python 货币/通胀模型，先 A 后 B）。
- 仓库：`Justinjchen-Cornell/Ledger-of-Empires`，public，`main`。
- 亲子线：8 个故事，一个内核一个；主角“砖砖”；磁力片当教具。
- 测试目录：统一根 `tests/`，不分散。
```

`00-总控/术语表.md`: 8 内核定义 + 关键术语（硬锚点、区间估计、失效条件、反事实、费曼测试）。

- [ ] **Step 4: 运行测试，确认通过**

Run: `pytest tests/test_repo_skeleton.py -q`
Expected: PASS（3 passed）。

- [ ] **Step 5: Commit**

```bash
git add README.md LICENSE LICENSE-CONTENT requirements.txt pytest.ini conftest.py 00-总控 tests/test_repo_skeleton.py
git commit -m "chore: add repo skeleton and governance files"
```


---

### Task 1: 清洗书 2 并切分两本书

**Files:**
- Create: `scripts/clean_book2.py`
- Create: `scripts/split_chapters.py`
- Test: `tests/test_clean_book2.py`
- Test: `tests/test_split_chapters.py`

**Interfaces:**
- Consumes: 原书 md 文件（vault 内，不在仓库）。
- Produces: `_private/books/book1/ch01-ch12.md`、`_private/books/book2/ch01-ch12.md`，带 frontmatter。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_clean_book2.py
from scripts.clean_book2 import clean_book2

def test_removes_toc_and_markup():
    raw = """::: sgc-toc-title
目录
:::

[第1章 东京梦华](#text00003.html)

# 第1章 东京梦华 {.bodycontent-first-title}

![](Image00000.jpg)

正文[]{#text00003.html}

## 小节 {#sigil_toc_id_1 .bodycontent-second-title}

更多
"""
    out = clean_book2(raw)
    assert out.startswith("# 第1章 东京梦华")
    assert "正文" in out
    assert ":::" not in out
    assert "[]{#" not in out
    assert "Image00000" not in out
    assert ".bodycontent" not in out
```

```python
# tests/test_split_chapters.py
from scripts.split_chapters import split_book1, split_book2

def test_split_book1_skips_toc():
    text = "第一章\n\n第一章\nbody1\n第二章\nbody2\n"
    chapters = split_book1(text, toc_count=1)
    assert len(chapters) == 2
    assert "body1" in chapters[0]["body"]
    assert chapters[1]["chapter"] == 2

def test_split_book2_uses_h1_headings():
    text = "# 第1章 A\nbody1\n# 第2章 B\nbody2\n"
    chapters = split_book2(text)
    assert len(chapters) == 2
    assert chapters[0]["title"] == "东京梦华"
    assert "body2" in chapters[1]["body"]
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `pytest tests/test_clean_book2.py tests/test_split_chapters.py -q`
Expected: FAIL，模块不存在。

- [ ] **Step 3: 实现 `scripts/clean_book2.py`**

```python
from pathlib import Path
import argparse
import re


def clean_book2(text: str) -> str:
    match = re.search(r"^# 第\d+章", text, flags=re.M)
    if not match:
        raise ValueError("no body chapter heading found")
    text = text[match.start():]
    text = re.sub(r"\[\]\{#[^}]+\}", "", text)
    text = re.sub(r"\s*\{(?:#[^}]+|\.[^}]+)\}", "", text)
    text = re.sub(r"!\[\]\([^)]*\)", "", text)
    text = re.sub(r"^:::.*$", "", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    src = Path(args.input).read_text(encoding="utf-8")
    out = clean_book2(src)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(out, encoding="utf-8")
    print(f"wrote {args.output} ({len(out)} chars)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 实现 `scripts/split_chapters.py`**

```python
from pathlib import Path
import argparse
import re

BOOK1_TITLES = [
    "此朝无钱胜有钱", "秦始皇统一了货币吗", "犯我货币者，虽强必诛",
    "迷失的货币", "国家与土匪", "铜钱三国志", "两晋衣冠", "南朝金粉",
    "大隋悲歌", "今有大唐初长成", "开元全盛日", "国在铜钱破",
]
BOOK2_TITLES = [
    "东京梦华", "宣战，以货币之名", "变法风云", "书画君臣", "错位的忠诚",
    "金钱恨，何时灭", "忽必烈和他的理财师们", "开河变钞祸根源",
    "朱重八的家庭经济学", "大明宝钞的玄机", "出局的大国", "白银帝国",
]


def _extract(lines, starts, titles, book):
    chapters = []
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        chapters.append({
            "book": book,
            "chapter": idx + 1,
            "title": titles[idx],
            "body": "\n".join(lines[start:end]).strip(),
            "start_line": start + 1,
            "end_line": end,
        })
    return chapters


def split_book1(text: str, toc_count: int = 12):
    lines = text.splitlines()
    starts = [
        i for i, line in enumerate(lines)
        if re.match(r"^第[一二三四五六七八九十]+章\s*$", line.strip())
    ]
    return _extract(lines, starts[toc_count:], BOOK1_TITLES, 1)


def split_book2(text: str):
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^# 第\d+章", line)]
    return _extract(lines, starts, BOOK2_TITLES, 2)


def write_chapters(chapters, out_dir: Path) -> None:
    for ch in chapters:
        book_dir = out_dir / f"book{ch['book']}"
        book_dir.mkdir(parents=True, exist_ok=True)
        path = book_dir / f"ch{ch['chapter']:02d}.md"
        frontmatter = (
            f"---\nbook: {ch['book']}\nchapter: {ch['chapter']}\n"
            f"title: {ch['title']}\nsource_start: {ch['start_line']}\n"
            f"source_end: {ch['end_line']}\n---\n\n"
        )
        path.write_text(frontmatter + ch["body"], encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    vault_root = project_root.parent
    book1 = vault_root / "08.投资决策框架/研究专题/金融史/中国是部金融史-透过金融读懂中国三千年 (陈雨露,杨忠恕).md"
    book2 = vault_root / "08.投资决策框架/研究专题/金融史/中国是部金融史2 (陈雨露  杨忠恕) (z-library.sk, 1lib.sk, z-lib.sk).md"

    parser = argparse.ArgumentParser()
    parser.add_argument("--book", choices=["1", "2", "all"], default="all")
    parser.add_argument("--out", default="_private/books")
    args = parser.parse_args()
    out_dir = project_root / args.out

    if args.book in ("1", "all"):
        write_chapters(split_book1(book1.read_text(encoding="utf-8")), out_dir)
    if args.book in ("2", "all"):
        from clean_book2 import clean_book2
        cleaned = clean_book2(book2.read_text(encoding="utf-8"))
        write_chapters(split_book2(cleaned), out_dir)
    print(f"done -> {out_dir}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 运行测试，确认通过**

Run: `pytest tests/test_clean_book2.py tests/test_split_chapters.py -q`
Expected: PASS（3 passed）。

- [ ] **Step 6: 在真实书上跑一遍**

Run:

```bash
python scripts/split_chapters.py --book all --out "_private/books"
find _private/books/book1 -name "ch*.md" | wc -l
find _private/books/book2 -name "ch*.md" | wc -l
```

Expected: 两个 `12`。

- [ ] **Step 7: Commit**

```bash
git add scripts/clean_book2.py scripts/split_chapters.py tests/test_clean_book2.py tests/test_split_chapters.py
git commit -m "feat(scripts): clean book2 and split chapters"
```


---

### Task 2: 模板与校验器

**Files:**
- Create: `templates/chapter.md`
- Create: `templates/card.md`
- Create: `templates/article.md`
- Create: `scripts/validate.py`
- Test: `tests/test_validate.py`

**Interfaces:**
- Consumes: 无。
- Produces: `validate_chapter(path) -> list[str]`、`validate_card(path) -> list[str]`、`validate_article(path) -> list[str]`；CLI `python scripts/validate.py --all`。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_validate.py
from scripts.validate import validate_chapter, validate_card, validate_article

CHAPTER = """---
book: 1
chapter: 1
title: 测试章
kernels: [K02]
status: done
estimated_minutes: 40
---

## 1. 本章定位
## 2. 三幕故事
## 3. 决策点
### 决策点 1
### 决策点 2
## 4. 五层追问
## 5. 原文摘句
> “引文一”（L100）
> “引文二”（L200）
> “引文三”（L300）
## 6. 数据与建模
## 7. 卡片草案
"""

CARD = """---
id: K02-01
kernel: K02
dynasty: 春秋
year: -685
title: 测试卡
evidence_grade: B
source_lines: [687]
hands_on: true
status: draft
---

## 处境
## 约束
## 选项
## 决策与结果
## 代价
## 机制
## 反事实
## 当代对照
## 失效条件
- 不可比一
- 不可比二
- 不可比三
## 我的异议
## 证据
- 等级：B
- 原文：L687
"""

ARTICLE = """---
title: 测试文章
chapters: [1, 2]
kernels: [K02]
status: draft
---

## 钩子
## 故事
## 机制
## 当代对照
## 失效条件
- 不可比：古代没有央行
## 反方
## 结论
"""

def test_valid_chapter_passes(tmp_path):
    p = tmp_path / "ch.md"
    p.write_text(CHAPTER, encoding="utf-8")
    assert validate_chapter(p) == []

def test_chapter_quote_needs_line_number(tmp_path):
    p = tmp_path / "ch.md"
    p.write_text(CHAPTER.replace("（L100）", ""), encoding="utf-8")
    assert any("line number" in e for e in validate_chapter(p))

def test_card_needs_three_failure_conditions(tmp_path):
    p = tmp_path / "card.md"
    p.write_text(CARD.replace("- 不可比三\n", ""), encoding="utf-8")
    assert any("failure conditions" in e for e in validate_card(p))

def test_valid_card_and_article_pass(tmp_path):
    c = tmp_path / "card.md"; c.write_text(CARD, encoding="utf-8")
    a = tmp_path / "article.md"; a.write_text(ARTICLE, encoding="utf-8")
    assert validate_card(c) == []
    assert validate_article(a) == []
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `pytest tests/test_validate.py -q`
Expected: FAIL，`scripts.validate` 不存在。

- [ ] **Step 3: 创建模板**

`templates/chapter.md`:

````markdown
---
book: 1
chapter: 1
title: 本章标题
kernels: [K01]
status: pending
estimated_minutes: 40
---

## 1. 本章定位

- 书里的位置：
- 对应内核：
- 预计时长：40min

## 2. 三幕故事

### 困局

### 抉择

### 代价

## 3. 决策点

### 决策点 1

- 选项 A：
- 选项 B：
- 历史选择：
- 结果：

### 决策点 2

- 选项 A：
- 选项 B：
- 历史选择：
- 结果：

## 4. 五层追问

### 事实层

### 机制层

### 反事实层

### 映射层

### 失效层

## 5. 原文摘句

> “第一条引文”（L000）

> “第二条引文”（L000）

> “第三条引文”（L000）

## 6. 数据与建模

- 数据表：
- 公式：
- 更新文件：

## 7. 卡片草案

- 卡片 ID：
- 一句话机制：
- 失效条件：
````

`templates/card.md`:

````markdown
---
id: K01-01
kernel: K01
dynasty: 西汉
year: -186
title: 卡名
evidence_grade: B
source_lines: [1634, 1665]
hands_on: true
status: draft
---

## 处境

## 约束

## 选项

## 决策与结果

## 代价

## 机制

## 反事实

## 当代对照

## 失效条件

- 不可比：
- 不可比：
- 不可比：

## 我的异议

## 证据

- 等级：B
- 原文：L1634, L1665
````

`templates/article.md`:

````markdown
---
title: 文章标题
chapters: [1, 2]
kernels: [K02]
status: draft
---

## 钩子

## 故事

## 机制

## 当代对照

## 失效条件

- 不可比：

## 反方

## 结论
````

- [ ] **Step 4: 实现 `scripts/validate.py`**

```python
from pathlib import Path
import argparse
import re
import sys

CHAPTER_FM = ["book", "chapter", "title", "kernels", "status", "estimated_minutes"]
CARD_FM = ["id", "kernel", "dynasty", "year", "title", "evidence_grade", "source_lines", "hands_on", "status"]
CHAPTER_SECTIONS = [
    "## 1. 本章定位", "## 2. 三幕故事", "## 3. 决策点", "## 4. 五层追问",
    "## 5. 原文摘句", "## 6. 数据与建模", "## 7. 卡片草案",
]
CARD_SECTIONS = [
    "## 处境", "## 约束", "## 选项", "## 决策与结果", "## 代价", "## 机制",
    "## 反事实", "## 当代对照", "## 失效条件", "## 我的异议", "## 证据",
]
ARTICLE_SECTIONS = [
    "## 钩子", "## 故事", "## 机制", "## 当代对照", "## 失效条件", "## 反方", "## 结论",
]


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data, text[end + 5:]


def count_bullets(body, heading):
    match = re.search(rf"{re.escape(heading)}\s*\n((?:- .*\n?)+)", body)
    if not match:
        return 0
    return len([
        line for line in match.group(1).splitlines()
        if line.strip().startswith("- ") and line.strip() != "-"
    ])


def validate_chapter(path):
    errors = []
    text = Path(path).read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    for key in CHAPTER_FM:
        if key not in fm:
            errors.append(f"missing frontmatter: {key}")
    for section in CHAPTER_SECTIONS:
        if section not in body:
            errors.append(f"missing section: {section}")
    if body.count("### 决策点") < 2:
        errors.append("need >=2 decision points (### 决策点)")
    quotes = [line[2:].strip() for line in body.splitlines() if line.startswith("> ")]
    if len(quotes) < 3:
        errors.append("need >=3 quotes starting with '> '")
    for quote in quotes:
        if len(quote) > 200:
            errors.append(f"quote too long ({len(quote)} chars): {quote[:30]}...")
        if not re.search(r"L\d+", quote):
            errors.append(f"quote missing line number (L123): {quote[:30]}...")
    return errors


def validate_card(path):
    errors = []
    text = Path(path).read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    for key in CARD_FM:
        if key not in fm:
            errors.append(f"missing frontmatter: {key}")
    for section in CARD_SECTIONS:
        if section not in body:
            errors.append(f"missing section: {section}")
    if count_bullets(body, "## 失效条件") < 3:
        errors.append("need >=3 failure conditions under '## 失效条件'")
    if "不可比" not in body:
        errors.append("failure conditions must mention '不可比'")
    return errors


def validate_article(path):
    errors = []
    text = Path(path).read_text(encoding="utf-8")
    _, body = parse_frontmatter(text)
    for section in ARTICLE_SECTIONS:
        if section not in body:
            errors.append(f"missing section: {section}")
    if "不可比" not in body:
        errors.append("article needs at least one '不可比'")
    if "反方" not in body:
        errors.append("article needs a counterargument")
    return errors


def collect(paths, validator):
    errors = []
    for path in paths:
        errors.extend(f"{path}: {error}" for error in validator(path))
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", action="append", default=[])
    parser.add_argument("--card", action="append", default=[])
    parser.add_argument("--article", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    errors = []
    errors += collect(args.chapter, validate_chapter)
    errors += collect(args.card, validate_card)
    errors += collect(args.article, validate_article)

    if args.all:
        errors += collect(sorted(Path("01-章节").rglob("*.md")), validate_chapter)
        errors += collect(sorted(Path("02-卡片").rglob("*.md")), validate_card)
        errors += collect(sorted(Path("05-输出/文章").rglob("*.md")), validate_article)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 运行测试，确认通过**

Run: `pytest tests/test_validate.py -q`
Expected: PASS（4 passed）。

- [ ] **Step 6: Commit**

```bash
git add templates scripts/validate.py tests/test_validate.py
git commit -m "feat(validate): add content templates and validator"
```


---

### Task 3: 数据表、出处登记、数据字典

**Files:**
- Create: `03-数据/processed/dynasty_master.csv`
- Create: `03-数据/processed/fiscal_annual.csv`
- Create: `03-数据/processed/money_series.csv`
- Create: `03-数据/processed/price_series.csv`
- Create: `03-数据/processed/modern_series.csv`
- Create: `03-数据/sources.md`
- Create: `03-数据/data-dictionary.md`
- Test: `tests/test_data_schema.py`

**Interfaces:**
- Consumes: 无。
- Produces: 5 张 CSV + `sources.md` + `data-dictionary.md`，供 Task 4 的数据管道读取。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_data_schema.py
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "03-数据/processed"

EXPECTED = {
    "dynasty_master": ["period_id", "dynasty", "start_year", "end_year", "currency_regime", "land_system", "tax_system", "notes"],
    "fiscal_annual": ["period_id", "year", "revenue_land", "revenue_poll", "revenue_commerce", "revenue_monopoly", "expense_military", "expense_salary", "expense_court", "expense_tribute", "expense_public_works", "deficit", "financing_method", "source_id", "evidence_grade"],
    "money_series": ["period_id", "year", "coin_name", "weight_g", "fineness", "nominal_value", "issue_volume", "price_index", "silver_copper_ratio", "source_id", "evidence_grade"],
    "price_series": ["period_id", "year", "good", "unit", "price_nominal", "price_grams_silver", "source_id", "evidence_grade"],
    "modern_series": ["year", "gdp", "fiscal_revenue", "fiscal_expenditure", "m2", "land_sale_revenue", "external_reserves", "source"],
}

def test_headers():
    for name, cols in EXPECTED.items():
        df = pd.read_csv(DATA / f"{name}.csv")
        assert list(df.columns) == cols, name

def test_source_ids_exist():
    sources = (ROOT / "03-数据/sources.md").read_text(encoding="utf-8")
    for name in ["fiscal_annual", "money_series", "price_series"]:
        df = pd.read_csv(DATA / f"{name}.csv")
        for sid in df["source_id"].dropna():
            assert sid in sources, f"{name}: {sid}"

def test_evidence_grades():
    for name in ["fiscal_annual", "money_series", "price_series"]:
        df = pd.read_csv(DATA / f"{name}.csv")
        assert set(df["evidence_grade"].dropna()).issubset({"A", "B", "C"})
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `pytest tests/test_data_schema.py -q`
Expected: FAIL，CSV 不存在。

- [ ] **Step 3: 创建 5 张 CSV**

`03-数据/processed/dynasty_master.csv`:

```csv
period_id,dynasty,start_year,end_year,currency_regime,land_system,tax_system,notes
HAN_WEST,西汉,-202,8,荚钱→四铢→五铢,名田/限田,十五税一,吕后时期大通胀
XIN,新朝,9,23,宝货制,王田制,五均六筦,王莽币改
EASTERN_HAN,东汉,25,220,五铢,豪强兼并,田租/算赋,四出五铢
```

`03-数据/processed/fiscal_annual.csv`（15 列；空值留空）:

```csv
period_id,year,revenue_land,revenue_poll,revenue_commerce,revenue_monopoly,expense_military,expense_salary,expense_court,expense_tribute,expense_public_works,deficit,financing_method,source_id,evidence_grade
HAN_WEST,-186,,,,,,,,,,,币改+通胀,S001,B
XIN,11,,,,,,,,,,,币改+官营,S002,B
```

`03-数据/processed/money_series.csv`:

```csv
period_id,year,coin_name,weight_g,fineness,nominal_value,issue_volume,price_index,silver_copper_ratio,source_id,evidence_grade
HAN_WEST,-186,荚钱,,,,,,,S001,B
XIN,11,宝货制,,,,,,,S002,B
EASTERN_HAN,190,四出五铢,,,,,,,S003,B
```

`03-数据/processed/price_series.csv`:

```csv
period_id,year,good,unit,price_nominal,price_grams_silver,source_id,evidence_grade
XIN,11,谷,石,10000,,S002,B
EASTERN_HAN,190,谷,斛,1000000,,S003,B
```

`03-数据/processed/modern_series.csv`:

```csv
year,gdp,fiscal_revenue,fiscal_expenditure,m2,land_sale_revenue,external_reserves,source
2025,19498039388042.6,,,,,,World Bank NY.GDP.MKTP.CD
```

- [ ] **Step 4: 创建 `03-数据/sources.md`**

```markdown
# 数据出处

| id | 作者/来源 | 书名/报告 | 年份 | 位置 | 等级 | 备注 |
|---|---|---|---|---|---|---|
| S001 | 陈雨露、杨忠恕 | 中国是部金融史 | 2013 | 书1 L1634, L1665, L1779 | B | 汉初大通胀；三年贬值三十倍 |
| S002 | 陈雨露、杨忠恕 | 中国是部金融史 | 2013 | 书1 L2493 | B | 王莽第三次币改；谷价万钱/石 |
| S003 | 陈雨露、杨忠恕 | 中国是部金融史 | 2013 | 书1 L2951 | B | 董卓无字小钱；谷价百万钱/斛 |
| S004 | 陈雨露、杨忠恕 | 中国是部金融史2 | 2014 | 书2 L802-L830 | B | 交子起源 |
| S005 | World Bank | GDP (current US$) | 2026 | API NY.GDP.MKTP.CD | A | 2025 年中国 GDP |
```

- [ ] **Step 5: 创建 `03-数据/data-dictionary.md`**

写明 5 张表的字段、单位、允许值与空值规则：

- `dynasty_master`：一行一个朝代/时期；`period_id` 唯一。
- `fiscal_annual`：一行一个年份；收入/支出单位统一为“万石/万贯/万两”，在 `notes` 注明。
- `money_series`：`weight_g` 克；`fineness` 0-1；`price_index` 以某年为 100。
- `price_series`：`unit` 为石/斛/匹；`price_nominal` 为名义货币单位。
- `modern_series`：GDP 为现价美元；财政收支为人民币亿元；M2 为人民币亿元。
- 空值表示“史料未载”，不允许填 0。

- [ ] **Step 6: 运行测试，确认通过**

Run: `pytest tests/test_data_schema.py -q`
Expected: PASS（3 passed）。

- [ ] **Step 7: Commit**

```bash
git add 03-数据 tests/test_data_schema.py
git commit -m "feat(data): add schemas, sources, and data dictionary"
```


---

### Task 4: 数据管道 v0

**Files:**
- Create: `04-模型/python/data_pipeline.py`
- Test: `tests/test_data_pipeline.py`

**Interfaces:**
- Consumes: Task 3 的 5 张 CSV。
- Produces: `load_csv(path)`、`validate_schema(df, required)`、`save_processed(df, path)`、`run(data_dir)`。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_data_pipeline.py
import sys
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "04-模型/python"))
import data_pipeline

def test_validate_schema_missing_column():
    df = pd.DataFrame({"period_id": ["X"]})
    with pytest.raises(ValueError):
        data_pipeline.validate_schema(df, ["period_id", "year"])

def test_run_on_sample(tmp_path):
    for name, cols in data_pipeline.SCHEMAS.items():
        pd.DataFrame({c: [] for c in cols}).to_csv(tmp_path / f"{name}.csv", index=False)
    data_pipeline.run(tmp_path)
    assert (tmp_path / "dynasty_master.csv").exists()
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `pytest tests/test_data_pipeline.py -q`
Expected: FAIL，模块不存在。

- [ ] **Step 3: 实现 `04-模型/python/data_pipeline.py`**

```python
from pathlib import Path
import argparse
import pandas as pd

SCHEMAS = {
    "dynasty_master": ["period_id", "dynasty", "start_year", "end_year", "currency_regime", "land_system", "tax_system", "notes"],
    "fiscal_annual": ["period_id", "year", "revenue_land", "revenue_poll", "revenue_commerce", "revenue_monopoly", "expense_military", "expense_salary", "expense_court", "expense_tribute", "expense_public_works", "deficit", "financing_method", "source_id", "evidence_grade"],
    "money_series": ["period_id", "year", "coin_name", "weight_g", "fineness", "nominal_value", "issue_volume", "price_index", "silver_copper_ratio", "source_id", "evidence_grade"],
    "price_series": ["period_id", "year", "good", "unit", "price_nominal", "price_grams_silver", "source_id", "evidence_grade"],
    "modern_series": ["year", "gdp", "fiscal_revenue", "fiscal_expenditure", "m2", "land_sale_revenue", "external_reserves", "source"],
}


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str)


def validate_schema(df: pd.DataFrame, required: list[str]) -> bool:
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    return True


def save_processed(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def run(data_dir: Path) -> None:
    for name, required in SCHEMAS.items():
        path = data_dir / f"{name}.csv"
        df = load_csv(path)
        validate_schema(df, required)
        save_processed(df, path)
        print(f"{name}: {len(df)} rows")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="03-数据/processed")
    args = parser.parse_args()
    run(Path(args.data_dir))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行测试，确认通过**

Run: `pytest tests/test_data_pipeline.py -q`
Expected: PASS（2 passed）。

- [ ] **Step 5: 在真实数据上跑一遍**

Run: `python 04-模型/python/data_pipeline.py --data-dir 03-数据/processed`
Expected: 5 行输出，每张表 `N rows`。

- [ ] **Step 6: Commit**

```bash
git add 04-模型/python/data_pipeline.py tests/test_data_pipeline.py
git commit -m "feat(data): add v0 pipeline"
```

---

### Task 5: Excel 骨架

**Files:**
- Create: `04-模型/python/build_excel.py`
- Create: `04-模型/excel/王朝资产负债表.xlsx`（脚本生成）
- Test: `tests/test_excel_skeleton.py`

**Interfaces:**
- Consumes: 无。
- Produces: `build_workbook(path)`，生成含 `总表`、`K01`-`K08`、`情景`、`敏感性`、`数据字典` 的工作簿。

- [ ] **Step 1: 写失败测试**

```python
# tests/test_excel_skeleton.py
import sys
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "04-模型/python"))
import build_excel

def test_build_workbook(tmp_path):
    path = tmp_path / "test.xlsx"
    build_excel.build_workbook(path)
    wb = load_workbook(path)
    assert "总表" in wb.sheetnames
    assert "K01" in wb.sheetnames
    assert "K08" in wb.sheetnames
    assert "情景" in wb.sheetnames
    assert wb["总表"]["A1"].value == "王朝资产负债表"
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `pytest tests/test_excel_skeleton.py -q`
Expected: FAIL，模块不存在。

- [ ] **Step 3: 实现 `04-模型/python/build_excel.py`**

```python
from pathlib import Path
from openpyxl import Workbook

SHEETS = ["总表"] + [f"K{i:02d}" for i in range(1, 9)] + ["情景", "敏感性", "数据字典"]


def build_workbook(path: Path) -> Path:
    wb = Workbook()
    wb.remove(wb.active)
    for name in SHEETS:
        ws = wb.create_sheet(name)
        ws["A1"] = name

    summary = wb["总表"]
    summary["A1"] = "王朝资产负债表"
    for col, value in enumerate(["项目", "金额", "单位", "来源"], start=1):
        summary.cell(row=3, column=col, value=value)

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    out = project_root / "04-模型/excel/王朝资产负债表.xlsx"
    build_workbook(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行测试，确认通过**

Run: `pytest tests/test_excel_skeleton.py -q`
Expected: PASS（1 passed）。

- [ ] **Step 5: 生成真实工作簿**

Run: `python 04-模型/python/build_excel.py`
Expected: `wrote .../04-模型/excel/王朝资产负债表.xlsx`

- [ ] **Step 6: Commit**

```bash
git add 04-模型/python/build_excel.py 04-模型/excel/王朝资产负债表.xlsx tests/test_excel_skeleton.py
git commit -m "feat(model): add excel skeleton"
```


---

## Chapter Loop（Task 6-11 共用）

> 下面的 `chYY`、`KXX` 是循环变量；实际文件名见每个 Task 的 Files 块。

每个章节任务按以下 8 步执行。**Step 5 必须暂停，等用户回答后才继续。**

1. 读 `_private/books/bookX/chYY.md`（Task 1 已生成）。
2. 用 `templates/chapter.md` 起草 `01-章节/.../chYY-标题.md`。
   - 三幕故事必须包含：困局（场景 + 数字）、抉择（2-3 条路）、代价（短期 / 长期）。
   - 五层追问每层至少 1 个问题。
   - 至少 3 条原文摘句，行号用原书行号。
3. 找引文行号：

```bash
grep -n "关键词" "08.投资决策框架/研究专题/金融史/中国是部金融史-透过金融读懂中国三千年 (陈雨露,杨忠恕).md"
```

4. 校验章节包：

```bash
python scripts/validate.py --chapter "01-章节/.../chYY-标题.md"
```

Expected: `OK`。

5. **暂停**：把三幕故事 + 2-3 个决策点发给用户；等用户选择 / 回答。不要替用户选。
6. 用户回答后，用 `templates/card.md` 写卡片 `02-卡片/KXX-.../card-YY-标题.md`。
   - 必须包含用户的原始选择（可引用）。
   - 失效条件 ≥3，且至少 1 条写“不可比”。
   - “我的异议”必须写作者可能忽略的因素。
7. 校验卡片：

```bash
python scripts/validate.py --card "02-卡片/.../card-YY-标题.md"
```

Expected: `OK`。

8. 更新 `00-总控/进度表.md`（状态 `done`，填卡片 ID、文章 ID），commit：

```bash
git add "01-章节" "02-卡片" "00-总控/进度表.md"
git commit -m "feat(chYY): add chapter package and card KXX-YY"
```

---

### Task 6: 第 1 章《此朝无钱胜有钱》

**Files:**
- Create: `01-章节/书1-中国是部金融史/ch01-此朝无钱胜有钱.md`
- Create: `02-卡片/K02-官营垄断/card-01-管仲的刀.md`

**Parameters:**
- 原文：`_private/books/book1/ch01.md`（原书 L487-L1016）
- 内核：K02 官营垄断 / K03 土地财政
- 卡片：`K02-01` 管仲的刀
- 引文搜索词：`管仲告诉我们`（L687）、`齐桓公这辈子就做对了一件事`（L699）、`天下非一人之天下`（L969）
- 文章：无（第 1 篇在 Task 7）

- [ ] **Step 1-8: 按 Chapter Loop 执行**

- [ ] **Step 9: 额外验收**

用户能回答：管仲的“官营”到底解决了齐桓公的什么问题？代价是什么？

- [ ] **Step 10: Commit**

```bash
git add "01-章节/书1-中国是部金融史/ch01-此朝无钱胜有钱.md" "02-卡片/K02-官营垄断/card-01-管仲的刀.md" "00-总控/进度表.md"
git commit -m "feat(ch01): add chapter package and card K02-01"
```

---

### Task 7: 第 2 章《秦始皇统一了货币吗》+ 第 1 篇文章

**Files:**
- Create: `01-章节/书1-中国是部金融史/ch02-秦始皇统一了货币吗.md`
- Create: `02-卡片/K01-铸币贬值/card-01-秦半两.md`
- Create: `05-输出/文章/01-管仲的刀与秦始皇的秤.md`

**Parameters:**
- 原文：`_private/books/book1/ch02.md`（原书 L1017-L1622）
- 内核：K01 铸币贬值 / K02 官营垄断
- 卡片：`K01-01` 秦半两：统一形制，未统一信用
- 引文搜索词：`半两`、`统一`、`货币`
- 文章：第 1 篇，覆盖 ch1-2，`chapters: [1, 2]`，`kernels: [K02, K01]`

- [ ] **Step 1-8: 按 Chapter Loop 执行**

- [ ] **Step 9: 写第 1 篇文章**

用 `templates/article.md`，1500-2500 字。必须回答：
1. 管仲和秦始皇分别用什么方式把货币变成国家工具？
2. 两次尝试为什么一个成功、一个留下隐患？
3. 今天哪一幕在重演？哪一条不可比？

```bash
python scripts/validate.py --article "05-输出/文章/01-管仲的刀与秦始皇的秤.md"
```

Expected: `OK`。

- [ ] **Step 10: Commit**

```bash
git add "01-章节/书1-中国是部金融史/ch02-秦始皇统一了货币吗.md" "02-卡片/K01-铸币贬值/card-01-秦半两.md" "05-输出/文章/01-管仲的刀与秦始皇的秤.md" "00-总控/进度表.md"
git commit -m "feat(ch02): add chapter package, card K01-01, and article 1"
```

---

### Task 8: 第 3 章《犯我货币者，虽强必诛》

**Files:**
- Create: `01-章节/书1-中国是部金融史/ch03-犯我货币者虽强必诛.md`
- Create: `02-卡片/K04-战争财政/card-01-汉武帝的战争账单.md`

**Parameters:**
- 原文：`_private/books/book1/ch03.md`（原书 L1623-L2100）
- 内核：K01 铸币贬值 / K04 战争财政
- 卡片：`K04-01` 汉武帝的战争账单
- 引文搜索词：`白鹿皮币`、`盐铁`、`算缗`、`军费`
- 文章：无（第 2 篇在 Task 9）

- [ ] **Step 1-8: 按 Chapter Loop 执行**

- [ ] **Step 9: 额外验收**

用户能画出汉武帝的“财政缺口 → 融资方式”链条：战争 → 军费 → 加税/卖官/官营/铸币 → 民间反应。

- [ ] **Step 10: Commit**

```bash
git add "01-章节/书1-中国是部金融史/ch03-犯我货币者虽强必诛.md" "02-卡片/K04-战争财政/card-01-汉武帝的战争账单.md" "00-总控/进度表.md"
git commit -m "feat(ch03): add chapter package and card K04-01"
```


---

### Task 9: 第 4 章《迷失的货币》+ 第 2 篇文章

**Files:**
- Create: `01-章节/书1-中国是部金融史/ch04-迷失的货币.md`
- Create: `02-卡片/K03-土地财政/card-01-王莽王田制.md`
- Create: `05-输出/文章/02-汉武帝的账单与王莽的币改.md`

**Parameters:**
- 原文：`_private/books/book1/ch04.md`（原书 L2101-L2580）
- 内核：K01 铸币贬值 / K03 土地财政 / K06 国家信贷
- 卡片：`K03-01` 王莽王田制
- 引文搜索词：`王田`、`宝货制`、`五均`、`六筦`
- 文章：第 2 篇，覆盖 ch3-4，`chapters: [3, 4]`，`kernels: [K04, K03]`

- [ ] **Step 1-8: 按 Chapter Loop 执行**

- [ ] **Step 9: 写第 2 篇文章**

用 `templates/article.md`，1500-2500 字。必须回答：
1. 汉武帝和王莽都“抢钱”，为什么汉武帝的帝国没崩，王莽的新朝崩了？
2. 两人的融资顺序有什么不同？（加税 / 官营 / 铸币 / 土地）
3. 今天哪一幕在重演？哪一条不可比？

```bash
python scripts/validate.py --article "05-输出/文章/02-汉武帝的账单与王莽的币改.md"
```

Expected: `OK`。

- [ ] **Step 10: Commit**

```bash
git add "01-章节/书1-中国是部金融史/ch04-迷失的货币.md" "02-卡片/K03-土地财政/card-01-王莽王田制.md" "05-输出/文章/02-汉武帝的账单与王莽的币改.md" "00-总控/进度表.md"
git commit -m "feat(ch04): add chapter package, card K03-01, and article 2"
```

---

### Task 10: 第 5 章《国家与土匪》

**Files:**
- Create: `01-章节/书1-中国是部金融史/ch05-国家与土匪.md`
- Create: `02-卡片/K07-钱荒金融抑制/card-01-东汉钱荒.md`

**Parameters:**
- 原文：`_private/books/book1/ch05.md`（原书 L2581-L3028）
- 内核：K03 土地财政 / K07 钱荒与金融抑制
- 卡片：`K07-01` 东汉钱荒
- 引文搜索词：`四出五铢`、`钱荒`、`通胀`
- 文章：无（第 3 篇在 Task 11）

- [ ] **Step 1-8: 按 Chapter Loop 执行**

- [ ] **Step 9: 额外验收**

用户能解释：为什么东汉的通货膨胀没有救得了帝国？钱荒和土地兼并是什么关系？

- [ ] **Step 10: Commit**

```bash
git add "01-章节/书1-中国是部金融史/ch05-国家与土匪.md" "02-卡片/K07-钱荒金融抑制/card-01-东汉钱荒.md" "00-总控/进度表.md"
git commit -m "feat(ch05): add chapter package and card K07-01"
```

---

### Task 11: 第 6 章《铜钱三国志》+ 第 3 篇文章

**Files:**
- Create: `01-章节/书1-中国是部金融史/ch06-铜钱三国志.md`
- Create: `02-卡片/K01-铸币贬值/card-02-董卓无字小钱.md`
- Create: `05-输出/文章/03-国家与土匪.md`

**Parameters:**
- 原文：`_private/books/book1/ch06.md`（原书 L3029-L3518）
- 内核：K01 铸币贬值 / K04 战争财政
- 卡片：`K01-02` 董卓无字小钱
- 引文搜索词：`无字小钱`、`董卓`、`百万钱`
- 文章：第 3 篇，覆盖 ch5-6，`chapters: [5, 6]`，`kernels: [K07, K01]`

- [ ] **Step 1-8: 按 Chapter Loop 执行**

- [ ] **Step 9: 写第 3 篇文章**

用 `templates/article.md`，1500-2500 字。必须回答：
1. 东汉到三国的财政退化，是“没钱”还是“收不上来”？
2. 董卓的无字小钱为什么是古代最高通胀纪录？
3. 今天哪一幕在重演？哪一条不可比？

```bash
python scripts/validate.py --article "05-输出/文章/03-国家与土匪.md"
```

Expected: `OK`。

- [ ] **Step 10: Commit**

```bash
git add "01-章节/书1-中国是部金融史/ch06-铜钱三国志.md" "02-卡片/K01-铸币贬值/card-02-董卓无字小钱.md" "05-输出/文章/03-国家与土匪.md" "00-总控/进度表.md"
git commit -m "feat(ch06): add chapter package, card K01-02, and article 3"
```

---

### Task 12: M1 复盘与打 tag

**Files:**
- Create: `07-复盘/里程碑-06.md`

- [ ] **Step 1: 跑全量校验**

```bash
pytest -q
python scripts/validate.py --all
```

Expected: 所有测试 PASS；`OK`。

- [ ] **Step 2: 写 `07-复盘/里程碑-06.md`**

```markdown
# 里程碑 06 — M1 复盘

## 交付

- 6 个章节包：ch01-ch06
- 6 张卡：K02-01、K01-01、K04-01、K03-01、K07-01、K01-02
- 3 篇文章：01、02、03
- 数据管道 v0、Excel 骨架
- 测试与校验器

## 指标

- 每章实际用时：
- 用户决策点互动次数：
- 卡片一次通过率：
- 文章字数：
- 校验器一次通过率：

## 什么有效

## 什么无效

## 决策

- [ ] 继续全量（24 章）
- [ ] 缩回 MVP（6 卡）
- [ ] 调整节奏

## 下一步

写 M2 计划（ch7-12 + 模型 A v1 + 工作台骨架 + 4 个亲子故事）。
```

- [ ] **Step 3: Commit 并打 tag**

```bash
git add "07-复盘/里程碑-06.md"
git commit -m "docs: add M1 review"
git tag v0.1-M1
```

- [ ] **Step 4: 推送（用户确认后）**

```bash
git push origin main
git push origin v0.1-M1
```

Expected: 远端出现 `main` 和 `v0.1-M1`。

---

## Self-Review

**Spec coverage**

| Spec 章节 | 对应 Task |
|---|---|
| 1 目标 / 2 范围 | Task 0 作战卡、Task 12 复盘 |
| 3 学习闭环 | Chapter Loop、Task 6-11 |
| 4 项目结构 | Task 0、Task 1、Task 3 |
| 5 数据与模型 | Task 3、Task 4、Task 5 |
| 6 产出流水线 | Task 6-11（卡片 / 文章）；M2-M4 另写计划 |
| 7 变现与公开 | Task 0 README / 决策日志；M4 执行 |
| 8 节奏与里程碑 | Chapter Loop、Task 12 |
| 9 风险与对策 | Global Constraints |
| 10 验收 / DoD | Task 2 校验器、Task 12 复盘 |

**Placeholder scan:** 无 TBD / TODO；内容任务的正文由执行者在 Chapter Loop 中生成，结构、引文行号、验收标准均已固定。

**Type consistency:** `validate_chapter` / `validate_card` / `validate_article` 在 Task 2 定义，Task 6-11 调用；`SCHEMAS` 在 Task 3 和 Task 4 中同名同字段。

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-10-25-m1-foundation.md`.**

两种执行方式：

1. **Subagent-Driven（推荐）**：每个 Task 派一个新 subagent，Task 之间做两阶段 review，迭代快。
2. **Inline Execution**：在本会话里按 `executing-plans` 批量执行，带 checkpoint。

选哪种？
