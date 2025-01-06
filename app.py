import streamlit as st
import pandas as pd
import pycountry
import phonenumbers

# App title
st.title("Pakistani Executive Forum")

# Initialize the database in session state (hidden in background)
if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame(columns=[
        "First Name", "Last Name", "Contact #", "Country of Residence", 
        "LinkedIn URL", "Sector / Industry", "Position", "Areas of Collaboration"
    ])

# Input Form
with st.form("user_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    # Country dropdown
    countries = [country.name for country in pycountry.countries]
    country = st.selectbox("Country of Residence", options=["Select a country"] + countries)
    
    # Auto-populate contact number country code
    if country and country != "Select a country":
        country_code = pycountry.countries.get(name=country).alpha_2
        contact_code = phonenumbers.COUNTRY_CODE_TO_REGION_CODE.get(country_code, "")
        contact = st.text_input(f"Contact # (+{contact_code if contact_code else ''})")
    else:
        contact = st.text_input("Contact #")
        
    linkedin = st.text_input("LinkedIn URL")
    industry = st.text_input("Industry")
    position = st.text_input("Position")
    collaboration = st.text_area("Areas of Collaboration")
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    # Update the database in the background (hidden)
    new_entry = pd.DataFrame([{
        "First Name": first_name,
        "Last Name": last_name,
        "Contact #": contact,
        "Country of Residence": country,
        "LinkedIn URL": linkedin,
        "Industry": industry,
        "Position": position,
        "Areas of Collaboration": collaboration,
    }])
    
    st.session_state.database = pd.concat([st.session_state.database, new_entry], ignore_index=True)
    st.success("Your data has been added successfully!")
    
    # Clear input fields after submission
    st.experimental_rerun()  # This forces a re-run of the app, clearing the input fields

# Save button (optional, for download or backup)
if st.button("Save Database"):
    st.session_state.database.to_csv("database.csv", index=False)
    st.success("Database saved to database.csv!")

# Footer
st.markdown("---")
st.markdown("<center>A tool to facilitate interaction among PEF members by Khalid Baig</center>", unsafe_allow_html=True)
