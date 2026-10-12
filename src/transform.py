
import pandas as pd
from pathlib import Path

# Locate the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output file paths
input_file = BASE_DIR / "data" / "extracted_orders.csv"
output_file = BASE_DIR / "data" / "cleaned_orders.csv"

# 1. Read the extracted data
df = pd.read_csv(input_file)

print("Original rows:", len(df))

# 2. Remove duplicate order IDs
df = df.drop_duplicates(subset=["order_id"])

# 3. Remove rows missing required information
required_columns = [
    "order_id", "customer_id", "product",
    "quantity", "price", "status"
]
df = df.dropna(subset=required_columns)

# 4. Convert numeric columns to numeric values
df["quantity"] = pd.to_numeric(
    df["quantity"], errors="coerce"
)
df["price"] = pd.to_numeric(
    df["price"], errors="coerce"
)

# 5. Remove invalid quantities and prices
df = df.dropna(subset=["quantity", "price"])
df = df[(df["quantity"] > 0) & (df["price"] >= 0)]

# 6. Clean text fields
df["product"] = df["product"].str.strip()
df["status"] = df["status"].str.strip().str.title()

# 7. Calculate the total order amount
df["total_amount"] = df["quantity"] * df["price"]

# 8. Save the transformed data
df.to_csv(output_file, index=False)

print("Cleaned rows:", len(df))
print("Cleaned data saved to:", output_file)
print("\nCleaned data:")
print(df.head())
