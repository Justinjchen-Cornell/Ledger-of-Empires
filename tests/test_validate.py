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
