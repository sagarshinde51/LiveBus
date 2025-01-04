import streamlit as st
import mysql.connector
from mysql.connector import OperationalError, IntegrityError
import io

# MySQL database connection details
host = "82.180.143.66"
user = "u263681140_students"
passwd = "testStudents@123"
db_name = "u263681140_students"

# Function to fetch data from BusPass table based on RFID
def fetch_data_from_buspass(rfid=None):
    try:
        # Establishing connection to the database using mysql.connector
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Query to fetch all data from BusPass table or filter by RFID
        if rfid:
            query = f"SELECT * FROM BusPass WHERE RFID = '{rfid}'"
        else:
            query = "SELECT * FROM BusPass"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Fetching column names
        col_names = [desc[0] for desc in cursor.description]
        
        # Closing the connection
        cursor.close()
        conn.close()
        
        return col_names, rows
    except OperationalError as e:
        st.error(f"Database connection error: {e}")
        return None, None
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")
        return None, None

# Function to fetch data from BusPassangers table based on RFID and retrieve photo
def fetch_data_from_buspassangers(rfid):
    try:
        # Establishing connection to the database using mysql.connector
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Query to fetch data from BusPassangers table based on RFID
        query = f"SELECT * FROM BusPassangers WHERE RFID = '{rfid}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Fetching column names
        col_names = [desc[0] for desc in cursor.description]
        
        # Fetch the photo data from the table (assuming photo is the last column)
        photo_data = None
        if rows:
            photo_data = rows[0][-1]  # Last column is assumed to be the photo
        
        # Closing the connection
        cursor.close()
        conn.close()
        
        return col_names, rows, photo_data
    except OperationalError as e:
        st.error(f"Database connection error: {e}")
        return None, None, None
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")
        return None, None, None

# Streamlit app
st.title("Live Bus Passengers")

# Fetch BusPass data to display RFID options
col_names, rows = fetch_data_from_buspass()

if col_names and rows:
    # Display the data from BusPass table
    st.subheader("Current Passengers from Bus")
    buspass_df = [dict(zip(col_names, row)) for row in rows]
    st.table(buspass_df)

    # Create a list of RFID numbers from BusPass table
    rfid_numbers = [row[2] for row in rows]  # Assuming RFID is the second column
    selected_rfid = st.selectbox("Select RFID No", rfid_numbers)

    if selected_rfid:
        # Fetch and display BusPassangers data for the selected RFID
        st.subheader(f"Data for RFID {selected_rfid}")
        col_names, buspassangers_rows, photo_data = fetch_data_from_buspassangers(selected_rfid)

        if buspassangers_rows:
            buspassangers_df = [dict(zip(col_names, row)) for row in buspassangers_rows]
            st.table(buspassangers_df)
            
            # Show the photo when the button is clicked
            if photo_data:
                if st.button("View Photo"):
                    st.image(photo_data, caption="Passenger Photo", use_column_width=True)
        else:
            st.warning("No data found for the selected RFID.")
else:
    st.warning("No data retrieved or there was an error.")
