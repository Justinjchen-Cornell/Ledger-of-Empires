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
