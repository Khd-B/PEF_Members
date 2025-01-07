import streamlit as st
import sqlite3
import re
import pycountry
import phonenumbers

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


# Function to get country dial code
def get_country_dial_code(country_name):
    try:
        for region_code in phonenumbers.COUNTRY_CODE_TO_REGION_CODE:
            if country_name in phonenumbers.COUNTRY_CODE_TO_REGION_CODE[region_code]:
                return f"+{region_code}"
    except KeyError:
        return ""
    return ""


# Validation functions
def validate_contact_number(contact_number):
    pattern = re.compile(r'^\+\d{1,3}\d{9,12}$')
    return bool(pattern.match(contact_number))


def validate_linkedin_url(linkedin_url):
    pattern = re.compile(r'^https://www\.linkedin\.com/in/[\w-]+$')
    return bool(pattern.match(linkedin_url))


# App title
st.title("Professional Network App")

# Form inputs
with st.form("data_entry_form", clear_on_submit=True):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    # Country of Residence
    countries = [country.name for country in pycountry.countries]
    country_residence = st.selectbox("Country of Residence", countries)

    # Auto-fill country dial code
    dial_code = get_country_dial_code(country_residence)
    contact_number = st.text_input("Contact #", value=dial_code)

    linkedin_url = st.text_input("LinkedIn URL")
    you_are = st.multiselect("You are", ["Consultant", "Entrepreneur", "Executive", "Freelancer"])
    areas_collaboration = st.text_input("Areas of Potential Collaboration")

    # Submit button
    submitted = st.form_submit_button("Submit")

if submitted:
    if not first_name or not last_name or not validate_contact_number(contact_number):
        st.error("Please ensure all fields are filled correctly.")
    elif not validate_linkedin_url(linkedin_url):
        st.error("Please provide a valid LinkedIn URL.")
    else:
        # Prevent duplicate entries
        cursor.execute("""
            SELECT COUNT(*) FROM professionals
            WHERE first_name = ? AND last_name = ? AND contact_number = ?
        """, (first_name, last_name, contact_number))
        if cursor.fetchone()[0] > 0:
            st.warning("This entry already exists in the database.")
        else:
            # Insert data into the database
            cursor.execute("""
                INSERT INTO professionals (first_name, last_name, contact_number, country_residence, linkedin_url, you_are, areas_collaboration)
                VALUES (?, ?, ?, ?, ?, ?, ?);
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
    """, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    results = cursor.fetchall()
    if results:
        for row in results:
            st.write(row)
    else:
        st.write("No results found.")

if st.button("View All Records"):
    cursor.execute("SELECT * FROM professionals")
    results = cursor.fetchall()
    for row in results:
        st.write(row)


# Background image
st.markdown(r"""
<style>
.reportview-container {
    background: url("https://raw.githubusercontent.com/Khd-B/PEF_Members/main/PEF Logo.jpg") no-repeat center fixed;
    background-size: cover;
}
</style>
""", unsafe_allow_html=True)
