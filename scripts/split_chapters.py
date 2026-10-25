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


def split_book1(text: str, toc_count: int | None = None):
    lines = text.splitlines()
    starts = [
        i for i, line in enumerate(lines)
        if re.match(r"^第[一二三四五六七八九十]+章\s*$", line.strip())
    ]
    if toc_count is None:
        toc_count = 12 if len(starts) >= 24 else 0
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
