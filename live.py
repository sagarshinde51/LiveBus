import streamlit as st
import mysql.connector
from mysql.connector import OperationalError, IntegrityError

# MySQL database connection details
host = "82.180.143.66"
user = "u263681140_students"
passwd = "testStudents@123"
db_name = "u263681140_students"

# Function to update the balance for a given RFID
def update_balance(rfid, additional_balance):
    try:
        # Connect to the MySQL database using mysql.connector
        conn = mysql.connector.connect(host=host, user=user, password=passwd, database=db_name)
        cursor = conn.cursor()

        # Check if the RFID exists and fetch the current balance
        cursor.execute("SELECT balance FROM BusPassangers WHERE RFID = %s", (rfid,))
        record = cursor.fetchone()

        if record:
            # Get the previous balance
            previous_balance = float(record[0])

            # Calculate the new balance
            new_balance = previous_balance + additional_balance

            # Update the balance in the database
            cursor.execute(
                "UPDATE BusPassangers SET balance = %s WHERE RFID = %s",
                (new_balance, rfid),
            )
            conn.commit()
            st.success(
                f"Balance for RFID {rfid} updated successfully.\n"
                f"Previous Balance: {previous_balance}, New Balance: {new_balance}"
            )
        else:
            st.error(f"No record found for RFID {rfid}.")
        
    except OperationalError as e:
        st.error(f"Database connection error: {e}")
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Streamlit user interface
st.title("Update Passenger Balance")
st.write("Enter RFID and additional balance to update the passenger's balance.")

# Input fields
rfid = st.text_input("Enter RFID:")
additional_balance = st.text_input("Enter Additional Balance:")

# Update button
if st.button("Update Balance"):
    if not rfid or not additional_balance:
        st.error("Both RFID and additional balance are required.")
    else:
        try:
            additional_balance = float(additional_balance)  # Ensure balance is numeric
            update_balance(rfid, additional_balance)
        except ValueError:
            st.error("Additional balance must be a numeric value.")
