import streamlit as st
import sqlite3
import re
import phonenumbers
import pycountry

# Create database connection
conn = sqlite3.connect("professionals.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS professionals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        contact_number TEXT,
        country_residence TEXT,
        linkedin_url TEXT,
        you_are TEXT,
        areas_collaboration TEXT
    );
""")
conn.commit()

# Function to get dialing code
def get_country_dial_code(country_name):
    try:
        country_code = pycountry.countries.get(name=country_name).alpha_2
        example_number = phonenumbers.example_number_for_region(country_code)
        dial_code = phonenumbers.format_number(example_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(' ')[0]
        return dial_code
    except Exception as e:
        return ""

def validate_contact_number(contact_number):
    pattern = re.compile(r'^\+\d{1,3}\d{9,12}$')
    return bool(pattern.match(contact_number))

def validate_linkedin_url(linkedin_url):
    pattern = re.compile(r'^https://www\.linkedin\.com/in/[\w-]+$')
    return bool(pattern.match(linkedin_url))

# App Title
st.title("Professional Network App")

# Input Form
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
country_residence = st.selectbox("Country of Residence", ["Select a country"] + [country.name for country in pycountry.countries])
contact_number = st.text_input("Contact #", value=get_country_dial_code(country_residence) if country_residence != "Select a country" else "")
linkedin_url = st.text_input("LinkedIn URL")
you_are = st.multiselect("You are", ["Consultant", "Entrepreneur", "Executive", "Freelancer"])
areas_collaboration = st.text_input("Areas of Potential Collaboration")

# Enable Submit Button
def enable_submit_button():
    return all([
        first_name, last_name, 
        country_residence != "Select a country", 
        contact_number, linkedin_url, you_are, areas_collaboration
    ])

# Submit Button
if st.button("Submit", disabled=not enable_submit_button()):
    # Validate inputs
    if not validate_contact_number(contact_number):
        st.error("Invalid contact number. Please include country code (e.g., +92).")
    elif not validate_linkedin_url(linkedin_url):
        st.error("Invalid LinkedIn URL. Please ensure it matches the format: https://www.linkedin.com/in/username.")
    else:
        cursor.execute("""
            INSERT OR IGNORE INTO professionals (first_name, last_name, contact_number, country_residence, linkedin_url, you_are, areas_collaboration)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            first_name, last_name, contact_number, country_residence, linkedin_url, ', '.join(you_are), areas_collaboration
        ))
        conn.commit()
        st.success("Your data has been saved successfully!")
        st.experimental_rerun()

# Reset Button
if st.button("Reset"):
    st.experimental_rerun()

# Search Functionality
search_term = st.text_input("Search for members")
if st.button("Search"):
    cursor.execute("""
        SELECT * FROM professionals 
        WHERE first_name LIKE ? OR last_name LIKE ? OR you_are LIKE ?;
    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    if results:
        for row in results:
            st.write(row)
    else:
        st.info("No results found.")

# View Database
if st.button("View Database"):
    cursor.execute("SELECT * FROM professionals")
    results = cursor.fetchall()
    for row in results:
        st.write(row)

# Background Image
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://raw.githubusercontent.com/Khd-B/PEF_Members/main/PEF Logo.jpg") no-repeat center fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
