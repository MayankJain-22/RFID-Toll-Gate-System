import serial
import mysql.connector
import subprocess
from datetime import datetime

# Open the monitoring scripts in separate CMD windows
subprocess.Popen(["start", "cmd", "/k", "python live_gate_entries.py"], shell=True)
subprocess.Popen(["start", "cmd", "/k", "python live_toll_transactions.py"], shell=True)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",          # Change if needed
    password="YOUR_PASSWORD",  # Replace with your MySQL password
    database="TollGate"
)
cursor = db.cursor()

# Connect to Arduino via Serial (Change COM5 to your correct port)
arduino = serial.Serial('COM5', 9600)

TOLL_AMOUNT = 50  # Set toll charge amount

print("RFID reader ready. Place your card...")  # Show this message only once

while True:
    if arduino.in_waiting:
        rfid_tag = arduino.readline().decode().strip()

        if len(rfid_tag) < 4:  # Ignore invalid data
            continue

        print(f"Scanned Tag: {rfid_tag}")

        # Get current time in 12-hour format
        current_time = datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')

        # Check if RFID tag exists in the database
        cursor.execute("SELECT balance FROM Users WHERE rfid_tag = %s", (rfid_tag,))
        result = cursor.fetchone()

        if result:
            balance = result[0]
            if balance >= TOLL_AMOUNT:
                new_balance = balance - TOLL_AMOUNT
                cursor.execute("UPDATE Users SET balance = %s WHERE rfid_tag = %s", (new_balance, rfid_tag))
                db.commit()

                # Log successful entry in Gate_Entries
                cursor.execute("INSERT INTO Gate_Entries (rfid_tag, entry_time, access_granted) VALUES (%s, %s, %s)",
                               (rfid_tag, current_time, "Yes"))
                db.commit()

                # Log the transaction in Toll_Transactions
                cursor.execute("INSERT INTO Toll_Transactions (rfid_tag, transaction_time, amount_deducted, balance_left) VALUES (%s, %s, %s, %s)",
                               (rfid_tag, current_time, TOLL_AMOUNT, new_balance))
                db.commit()

                print(f"✅ Access Granted. ₹{TOLL_AMOUNT} deducted. New Balance: ₹{new_balance}")
                arduino.write(b'OPEN')  # Send open signal to Arduino
            else:
                print("❌ Insufficient Balance")
                arduino.write(b'CLOSED')

                # Log denied entry in Gate_Entries
                cursor.execute("INSERT INTO Gate_Entries (rfid_tag, entry_time, access_granted) VALUES (%s, %s, %s)",
                               (rfid_tag, current_time, "No"))
                db.commit()
        else:
            print("⛔ Unauthorized Access")
            arduino.write(b'INVALID')

            # Log unauthorized entry in Gate_Entries
            cursor.execute("INSERT INTO Gate_Entries (rfid_tag, entry_time, access_granted) VALUES (%s, %s, %s)",
                           (rfid_tag, current_time, "No"))
            db.commit()
