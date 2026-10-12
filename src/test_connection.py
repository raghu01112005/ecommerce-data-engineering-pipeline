
import mysql.connector
from getpass import getpass

print("Connecting to MySQL...")

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=getpass("Enter your MySQL password:"),
        database="ecommerce_db",
        connection_timeout=10
    )

    print("SUCCESS: Python connected to MySQL!")

    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    print("MySQL version:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM orders")
    print("Number of orders:", cursor.fetchone()[0])

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("CONNECTION ERROR:", error)
