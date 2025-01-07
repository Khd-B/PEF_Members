import streamlit as st
import sqlite3
import re
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
        industry TEXT,
        areas_collaboration TEXT
    );
""")

conn.commit()


def get_country_code(country_name):
    countries = pycountry.countries
    for country in countries:
        if country.name == country_name:
            return country.alpha_2
    return None


def validate_contact_number(contact_number):
    pattern = re.compile(r'^\+\d{1,3}\d{9,12}$')
    return bool(pattern.match(contact_number))


def validate_linkedin_url(linkedin_url):
    pattern = re.compile(r'^https://www\.linkedin\.com/in/[\w-]+$')
    return bool(pattern.match(linkedin_url))


st.title("Professional Network App")


first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
country_residence = st.selectbox("Country of Residence", [country.name for country in pycountry.countries])
contact_number = st.text_input("Contact #", value="+" + get_country_code(country_residence))
linkedin_url = st.text_input("LinkedIn URL")
industry = st.multiselect("Industry", ["Consultant", "Businessman", "Executive", "Freelancer"])
areas_collaboration = st.text_input("Areas of Potential Collaboration")


def enable_submit_button():
    return (first_name and last_name and country_residence and validate_contact_number(contact_number) 
            and validate_linkedin_url(linkedin_url) and industry and areas_collaboration)


if st.button("Submit", disabled=not enable_submit_button()):
    confirmation = st.confirm_dialog("Confirm", "Are you sure you want to submit?")
    if confirmation:
        cursor.execute("""
            INSERT OR IGNORE INTO professionals (first_name, last_name, contact_number, country_residence, linkedin_url, industry, areas_collaboration)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (first_name, last_name, contact_number, country_residence, linkedin_url, ', '.join(industry), areas_collaboration))
        
        conn.commit()
        conn.close()
        
        # Clear input fields
        st.experimental_show("first_name", value="")
        st.experimental_show("last_name", value="")
        st.experimental_show("contact_number", value="")
        st.experimental_show("linkedin_url", value="")
        st.experimental_show("areas_collaboration", value="")


search_term = st.text_input("Search for members")
if st.button("Search"):
    cursor.execute("SELECT * FROM professionals WHERE first_name LIKE ? OR last_name LIKE ? OR industry LIKE ?", ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    results = cursor.fetchall()
    for row in results:
        st.write(row)


if st.button("View Database"):
    cursor.execute("SELECT * FROM professionals")
    results = cursor.fetchall()
    for row in results:
        st.write(row)


# Background image
st.markdown(r"""
<style>
.reportview-container {
    background: url("https://github.com/Khd-B/PEF_Members/blob/main/PEF%20Logo.jpg") no-repeat center fixed;
    background-size: cover;
}
</style>
""",
unsafe_allow_html=True,
)
