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
