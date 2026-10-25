from pathlib import Path
import argparse
import re
import sys

CHAPTER_FM = ["book", "chapter", "title", "kernels", "status", "estimated_minutes"]
CARD_FM = ["id", "kernel", "dynasty", "year", "title", "evidence_grade", "source_lines", "hands_on", "status"]
CHAPTER_SECTIONS = [
    "## 1. 本章定位", "## 2. 三幕故事", "## 3. 决策点", "## 4. 五层追问",
    "## 5. 原文摘句", "## 6. 数据与建模", "## 7. 卡片草案", "## 8. 核心总结",
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
