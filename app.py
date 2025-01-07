import streamlit as st
import sqlite3
import pycountry

# Database connection setup
DB_FILE = "professionals.db"

def create_database():
    """Create the database and table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professionals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            country_residence TEXT NOT NULL,
            linkedin_url TEXT,
            you_are TEXT NOT NULL,
            areas_collaboration TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

create_database()

# Set background with logo
st.markdown(
    """
    <style>
        .reportview-container {
            background: url(https://images.unsplash.com/photo-1574181397056-207efc36d6d9
) no-repeat center center fixed;
            background-size: cover;
            height: 100vh;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# App title
st.title("Professional Network App")

# Input form
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
country_residence = st.selectbox(
    "Country of Residence",
    ["Select a country"] + [country.name for country in pycountry.countries]
)
contact_number = st.text_input("Contact #")
linkedin_url = st.text_input("LinkedIn URL (Optional)")
you_are = st.multiselect(
    "You are",
    ["Consultant", "Entrepreneur", "Executive", "Freelancer"]
)
areas_collaboration = st.text_input("Areas of Potential Collaboration")

# Function to check if contact number already exists in the database
def check_contact_number_exists(contact_number):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM professionals WHERE contact_number = ?", (contact_number,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# Submit button
if st.button("Submit"):
    if not first_name or not last_name or country_residence == "Select a country" or not contact_number or not you_are or not areas_collaboration:
        st.error("All fields except LinkedIn URL are required!")
    elif check_contact_number_exists(contact_number):
        st.error("This contact number already exists. Please enter a different contact number.")
    else:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Insert the new entry
        cursor.execute("""
            INSERT INTO professionals (first_name, last_name, contact_number, country_residence, linkedin_url, you_are, areas_collaboration)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            first_name,
            last_name,
            contact_number,
            country_residence,
            linkedin_url,
            ', '.join(you_are),
            areas_collaboration
        ))
        conn.commit()
        conn.close()

        st.success("Your data has been added successfully!")

        # Reset the fields
        first_name = ""
        last_name = ""
        contact_number = ""
        linkedin_url = ""
        areas_collaboration = ""
        you_are = []
        
        # Show confirmation message
        st.info("Fields have been reset.")

# Search functionality
st.header("Search Members")
search_term = st.text_input("Search by name, role, or collaboration area")
if st.button("Search"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM professionals
        WHERE first_name LIKE ? OR last_name LIKE ? OR you_are LIKE ? OR areas_collaboration LIKE ?;
    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    conn.close()

    if results:
        for row in results:
            st.write(f"ID: {row[0]}")
            st.write(f"Name: {row[1]} {row[2]}")
            st.write(f"Contact: {row[3]}")
            st.write(f"Country: {row[4]}")
            st.write(f"LinkedIn: {row[5] if row[5] else 'N/A'}")
            st.write(f"You are: {row[6]}")
            st.write(f"Collaboration: {row[7]}")
            st.markdown("---")
    else:
        st.warning("No matching members found.")

# View all database records
if st.button("View All Members"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professionals")
    results = cursor.fetchall()
    conn.close()

    if results:
        for row in results:
            st.write(f"ID: {row[0]}")
            st.write(f"Name: {row[1]} {row[2]}")
            st.write(f"Contact: {row[3]}")
            st.write(f"Country: {row[4]}")
            st.write(f"LinkedIn: {row[5] if row[5] else 'N/A'}")
            st.write(f"You are: {row[6]}")
            st.write(f"Collaboration: {row[7]}")
            st.markdown("---")
    else:
        st.info("The database is empty.")

# Footer
st.markdown("---")
st.markdown("<center>Professional Network App by Khalid Baig</center>", unsafe_allow_html=True)
