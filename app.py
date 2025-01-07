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
