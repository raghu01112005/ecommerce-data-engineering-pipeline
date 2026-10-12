
import mysql.connector
import pandas as pd
from getpass import getpass
from pathlib import Path

# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent
output_dir = BASE_DIR / "data"
output_dir.mkdir(parents=True, exist_ok=True)

connection = None

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=getpass("Enter MySQL password: "),
        database="ecommerce_db"
    )

    # Extract orders from the database
    query = """
        SELECT
            order_id,
            customer_id,
            product,
            quantity,
            price,
            status
        FROM orders
    """

    df = pd.read_sql(query, connection)

    # Save extracted data
    output_file = output_dir / "extracted_orders.csv"
    df.to_csv(output_file, index=False)

    print("\nExtraction successful!")
    print("Rows extracted:", len(df))
    print("Output file:", output_file)
    print("\nExtracted records:")
    print(df.head())

except Exception as error:
    print("Extraction failed:", error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
