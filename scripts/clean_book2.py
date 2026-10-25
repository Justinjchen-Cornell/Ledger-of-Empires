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
