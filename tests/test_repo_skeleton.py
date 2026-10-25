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
