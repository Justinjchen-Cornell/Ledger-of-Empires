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
