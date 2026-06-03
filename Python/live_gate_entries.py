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

last_displayed_id = 0  # Track last displayed entry ID

def display_new_entries():
    global last_displayed_id

    while True:
        # Fetch only new entries since last update
        cursor.execute("SELECT * FROM Gate_Entries WHERE id > %s ORDER BY id ASC", (last_displayed_id,))
        new_entries = cursor.fetchall()

        if new_entries:
            for row in new_entries:
                print(f"| {row[0]:^5} | {row[1]:<10} | {row[2]:<18} | {row[3]:^14} |")
                last_displayed_id = row[0]  # Update last displayed ID

        time.sleep(2)  # Refresh every 2 seconds

# Print table headers once
print("\n📌 LIVE GATE ENTRIES 📌\n")
print("|  ID   | RFID Tag   | Time                   | Access Granted |")
print("----------------------------------------------------------------")

# Run live gate entry monitoring
display_new_entries()
