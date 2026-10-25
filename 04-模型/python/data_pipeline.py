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
