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
