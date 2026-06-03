import mysql.connector
import time

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",          # Change if needed
    password="YOUR_PASSWORD",  # Replace with your MySQL password
    database="TollGate",
    autocommit=True  # Enables instant updates
)
cursor = db.cursor()

last_displayed_id = 0  # Track last displayed transaction ID

def display_new_transactions():
    global last_displayed_id

    while True:
        # Fetch only new transactions since last update
        cursor.execute("SELECT * FROM Toll_Transactions WHERE id > %s ORDER BY id ASC", (last_displayed_id,))
        new_transactions = cursor.fetchall()

        if new_transactions:
            for row in new_transactions:
                print(f"{row[0]:<3} | {row[1]:<10} | {row[2]:<18} | ₹{row[3]:<7} | ₹{row[4]:<10}")
                last_displayed_id = row[0]  # Update last displayed ID

        time.sleep(2)  # Refresh every 2 seconds

# Print table headers once
print("📌 LIVE TOLL TRANSACTIONS 📌\n")
print("ID  |  RFID Tag  |          Time          | Deducted | Balance Left")
print("-------------------------------------------------------------------")

# Run live transaction monitoring
display_new_transactions()
