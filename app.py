import streamlit as st
import pandas as pd
import pycountry
import phonenumbers

# App title
st.title("Pakistani Executive Forum")

# Initialize the database in session state (hidden in background)
if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame(columns=[
        "Serial No.", "First Name", "Last Name", "Contact #", "Country of Residence", 
        "LinkedIn URL", "Sector / Industry", "Position", "Areas of Collaboration"
    ])

# Input Form
with st.form("user_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    # Country dropdown
    countries = [country.name for country in pycountry.countries]
    country = st.selectbox("Country of Residence", options=["Select a country"] + countries)
    
    # Auto-populate contact number country code using phonenumbers library
    contact = ""
    if country and country != "Select a country":
        try:
            # Get the country code from phonenumbers based on the country name
            country_obj = pycountry.countries.get(name=country)
            country_code = phonenumbers.country_code_for_region(country_obj.alpha_2)
            contact = st.text_input(f"Contact # (+{country_code})")
        except Exception as e:
            contact = st.text_input("Contact #")
            st.error("Unable to fetch country code")
    else:
        contact = st.text_input("Contact #")
        
    linkedin = st.text_input("LinkedIn URL")
    industry = st.text_input("Industry")
    position = st.text_input("Position")
    collaboration = st.text_area("Areas of Collaboration")
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    # Check if the data already exists to avoid duplication
    existing_data = st.session_state.database[
        (st.session_state.database["First Name"] == first_name) &
        (st.session_state.database["Last Name"] == last_name) &
        (st.session_state.database["Contact #"] == contact)
    ]
    
    if not existing_data.empty:
        st.warning("This entry already exists in the database!")
    else:
        # Generate serial number for the new entry (starting from 1)
        new_entry = pd.DataFrame([{
            "Serial No.": len(st.session_state.database) + 1,  # Serial starts from 1
            "First Name": first_name,
            "Last Name": last_name,
            "Contact #": contact,
            "Country of Residence": country,
            "LinkedIn URL": linkedin,
            "Industry": industry,
            "Position": position,
            "Areas of Collaboration": collaboration,
        }])
        
        # Update the database in the background (hidden)
        st.session_state.database = pd.concat([st.session_state.database, new_entry], ignore_index=True)
        st.success("Your data has been added successfully!")

        # Clear input fields after submission
        st.experimental_rerun()  # Forces a re-run, clearing input fields

# Footer
st.markdown("---")
st.markdown("<center>A tool to facilitate interaction among PEF members by Khalid Baig</center>", unsafe_allow_html=True)
