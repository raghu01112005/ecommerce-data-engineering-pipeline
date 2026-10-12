
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "cleaned_orders.csv"

df = pd.read_csv(file_path)

checks = {
    "Duplicate order IDs": df["order_id"].duplicated().sum(),
    "Missing values": df.isna().sum().sum(),
    "Invalid quantities": (df["quantity"] <= 0).sum(),
    "Negative prices": (df["price"] < 0).sum(),
    "Invalid order amounts": (
        df["total_amount"] != df["quantity"] * df["price"]
    ).sum()
}

print("DATA QUALITY REPORT")

for check, errors in checks.items():
    print(f"{check}: {errors}")

if all(errors == 0 for errors in checks.values()):
    print("\nAll data quality checks passed!")
else:
    print("\nData quality issues found!")
