
import mysql.connector
import pandas as pd
from getpass import getpass
from pathlib import Path

# Locate the project folder
BASE_DIR = Path(__file__).resolve().parent.parent
csv_file = BASE_DIR / "data" / "cleaned_orders.csv"

connection = None
cursor = None

try:
    # Read cleaned data
    df = pd.read_csv(csv_file)

    # Connect to MySQL
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=getpass("Enter MySQL password: "),
        database="ecommerce_db"
    )

    cursor = connection.cursor()

    # Create destination table
    create_table = """
    CREATE TABLE IF NOT EXISTS cleaned_orders (
        order_id INT PRIMARY KEY,
        customer_id INT NOT NULL,
        product VARCHAR(100) NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        status VARCHAR(30) NOT NULL,
        total_amount DECIMAL(12, 2) NOT NULL
    )
    """
    cursor.execute(create_table)

    # Prepare records from Pandas
    records = [
        (
            int(row.order_id),
            int(row.customer_id),
            row.product,
            int(row.quantity),
            float(row.price),
            row.status,
            float(row.total_amount)
        )
        for row in df.itertuples(index=False)
    ]

    # Replace destination contents safely for this starter project
    cursor.execute("DELETE FROM cleaned_orders")

    insert_query = """
    INSERT INTO cleaned_orders
    (order_id, customer_id, product, quantity,
     price, status, total_amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.executemany(insert_query, records)
    connection.commit()

    print("Data loaded successfully!")
    print("Rows loaded:", len(records))

    cursor.execute("SELECT COUNT(*) FROM cleaned_orders")
    print("Rows in MySQL:", cursor.fetchone()[0])

except Exception as error:
    if connection and connection.is_connected():
        connection.rollback()
    print("Loading failed:", error)

finally:
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
