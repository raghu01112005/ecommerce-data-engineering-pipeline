
import mysql.connector
from getpass import getpass

connection = None
cursor = None

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=getpass("Enter MySQL password: "),
        database="ecommerce_db"
    )

    cursor = connection.cursor()

    # Add any new customers
    cursor.execute("""
        INSERT INTO dim_customers (customer_id)
        SELECT DISTINCT c.customer_id
        FROM cleaned_orders AS c
        LEFT JOIN dim_customers AS d
            ON c.customer_id = d.customer_id
        WHERE d.customer_id IS NULL
    """)

    # Add any new products
    cursor.execute("""
        INSERT INTO dim_products (product_name, price)
        SELECT c.product, MAX(c.price)
        FROM cleaned_orders AS c
        LEFT JOIN dim_products AS p
            ON c.product = p.product_name
        WHERE p.product_id IS NULL
        GROUP BY c.product
    """)

    # Refresh fact data from the latest cleaned dataset
    cursor.execute("DELETE FROM fact_orders")

    cursor.execute("""
        INSERT INTO fact_orders (
            order_id,
            customer_id,
            product_id,
            quantity,
            price,
            total_amount,
            status
        )
        SELECT
            c.order_id,
            c.customer_id,
            p.product_id,
            c.quantity,
            c.price,
            c.total_amount,
            c.status
        FROM cleaned_orders AS c
        JOIN dim_products AS p
            ON c.product = p.product_name
    """)

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM fact_orders")
    total = cursor.fetchone()[0]

    print("Warehouse refresh successful!")
    print("Fact orders loaded:", total)

except Exception as error:
    if connection and connection.is_connected():
        connection.rollback()
    print("Warehouse refresh failed:", error)
    raise

finally:
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
