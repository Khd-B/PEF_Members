import streamlit as st
import sqlite3
import os
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

# App title
st.title("Professional Network App")

# Input form
with st.form("registration_form"):
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
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if not first_name or not last_name or country_residence == "Select a country" or not contact_number or not you_are or not areas_collaboration:
        st.error("All fields except LinkedIn URL are required!")
    else:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Check for duplicate entries
        cursor.execute("""
            SELECT COUNT(*) FROM professionals
            WHERE first_name = ? AND last_name = ? AND contact_number = ? AND country_residence = ?;
        """, (first_name, last_name, contact_number, country_residence))
        if cursor.fetchone()[0] > 0:
            st.warning("This entry already exists in the database.")
        else:
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
            st.success("Your data has been added successfully!")
        
        conn.close()

        # Clear input fields
        st.experimental_rerun()

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
import streamlit as st
import sqlite3
import pycountry
import phonenumbers
import re
import os  # Add this at the top of the file

# Option to reset the database
if st.button("Reset Database"):
    if os.path.exists("professionals.db"):
        os.remove("professionals.db")
        st.success("Database reset successfully! Please restart the app.")
    else:
        st.info("Database file does not exist. A new one will be created automatically.")

# Create or connect to the database
conn = sqlite3.connect("professionals.db")
cursor = conn.cursor()

# Create the professionals table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS professionals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        contact_number TEXT NOT NULL UNIQUE,
        country_residence TEXT NOT NULL,
        linkedin_url TEXT NOT NULL,
        you_are TEXT NOT NULL,
        areas_collaboration TEXT NOT NULL
    );
""")
conn.commit()

# Function to get the dial code for a country
def get_country_dial_code(country_name):
    try:
        for region_code, countries in phonenumbers.COUNTRY_CODE_TO_REGION_CODE.items():
            for country in countries:
                if pycountry.countries.get(alpha_2=country).name == country_name:
                    return f"+{region_code}"
    except Exception:
        return ""
    return ""

# Validation functions
def validate_contact_number(contact_number):
    pattern = re.compile(r'^\+\d{1,3}\d{9,12}$')
    return bool(pattern.match(contact_number))

def validate_linkedin_url(linkedin_url):
    pattern = re.compile(r'^https://www\.linkedin\.com/in/[\w-]+$')
    return bool(pattern.match(linkedin_url))

# Streamlit UI
st.title("Professional Network App")

# Form for data input
with st.form("data_entry_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    # Country selection and dialing code
    countries = [country.name for country in pycountry.countries]
    country_residence = st.selectbox("Country of Residence", countries)
    dial_code = get_country_dial_code(country_residence)
    contact_number = st.text_input("Contact #", value=dial_code)

    linkedin_url = st.text_input("LinkedIn URL")
    you_are = st.multiselect("You are", ["Consultant", "Entrepreneur", "Executive", "Freelancer"])
    areas_collaboration = st.text_input("Areas of Potential Collaboration")

    # Submit button
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    if not first_name or not last_name or not country_residence or not linkedin_url or not you_are or not areas_collaboration:
        st.error("All fields are required. Please fill them out.")
    elif not validate_contact_number(contact_number):
        st.error("Please enter a valid contact number (e.g., +1234567890).")
    elif not validate_linkedin_url(linkedin_url):
        st.error("Please enter a valid LinkedIn URL (e.g., https://www.linkedin.com/in/username).")
    else:
        # Check for duplicates
        cursor.execute("""
            SELECT COUNT(*) FROM professionals 
            WHERE first_name = ? AND last_name = ? AND contact_number = ?
        """, (first_name, last_name, contact_number))
        if cursor.fetchone()[0] > 0:
            st.warning("This record already exists in the database.")
        else:
            # Insert data into the database
            cursor.execute("""
                INSERT INTO professionals (first_name, last_name, contact_number, country_residence, linkedin_url, you_are, areas_collaboration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, contact_number, country_residence, linkedin_url, ', '.join(you_are), areas_collaboration))
            conn.commit()
            st.success("Your data has been added successfully!")

# Search and view database
st.subheader("Search for Members")
search_term = st.text_input("Search")
if st.button("Search"):
    cursor.execute("""
        SELECT * FROM professionals
        WHERE first_name LIKE ? OR last_name LIKE ? OR you_are LIKE ?
    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    if results:
        for row in results:
            st.write(row)
    else:
        st.info("No results found.")

if st.button("View All Records"):
    cursor.execute("SELECT * FROM professionals ORDER BY id ASC")
    results = cursor.fetchall()
    for row in results:
        st.write(row)

# Background image
st.markdown("""
<style>
    .reportview-container {
        background: url("https://raw.githubusercontent.com/Khd-B/PEF_Members/main/PEF Logo.jpg") no-repeat center fixed;
        background-size: cover;
    }
</style>
""", unsafe_allow_html=True)
