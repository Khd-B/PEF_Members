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

# Initialize form input fields in session state if not already present
if "first_name" not in st.session_state:
    st.session_state.first_name = ""
if "last_name" not in st.session_state:
    st.session_state.last_name = ""
if "contact" not in st.session_state:
    st.session_state.contact = ""
if "country" not in st.session_state:
    st.session_state.country = ""
if "linkedin" not in st.session_state:
    st.session_state.linkedin = ""
if "industry" not in st.session_state:
    st.session_state.industry = ""
if "position" not in st.session_state:
    st.session_state.position = ""
if "collaboration" not in st.session_state:
    st.session_state.collaboration = ""

# Input Form
with st.form("user_form"):
    st.session_state.first_name = st.text_input("First Name", value=st.session_state.first_name)
    st.session_state.last_name = st.text_input("Last Name", value=st.session_state.last_name)

    # Country dropdown
    countries = [country.name for country in pycountry.countries]
    st.session_state.country = st.selectbox("Country of Residence", options=["Select a country"] + countries, index=countries.index(st.session_state.country) if st.session_state.country else 0)
    
    # Auto-populate contact number country code using phonenumbers library
    contact = ""
    country_code = ""
    if st.session_state.country and st.session_state.country != "Select a country":
        try:
            # Get the country alpha_2 code from pycountry for the selected country
            country_obj = pycountry.countries.get(name=st.session_state.country)
            country_alpha_2 = country_obj.alpha_2
            
            # Use phonenumbers to fetch the country code for the country
            country_code = phonenumbers.country_code_for_region(country_alpha_2)
            st.session_state.contact = st.text_input(f"Contact # (+{country_code})", value=st.session_state.contact)
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state.contact = st.text_input("Contact #", value=st.session_state.contact)
    else:
        st.session_state.contact = st.text_input("Contact #", value=st.session_state.contact)
        
    st.session_state.linkedin = st.text_input("LinkedIn URL", value=st.session_state.linkedin)
    st.session_state.industry = st.text_input("Industry", value=st.session_state.industry)
    st.session_state.position = st.text_input("Position", value=st.session_state.position)
    st.session_state.collaboration = st.text_area("Areas of Collaboration", value=st.session_state.collaboration)
    
    # Submit button to submit the form data
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    # Check if the data already exists to avoid duplication
    existing_data = st.session_state.database[
        (st.session_state.database["First Name"] == st.session_state.first_name) &
        (st.session_state.database["Last Name"] == st.session_state.last_name) &
        (st.session_state.database["Contact #"] == st.session_state.contact)
    ]
    
    if not existing_data.empty:
        st.warning("This entry already exists in the database!")
    else:
        # Generate serial number for the new entry (starting from 1)
        new_entry = pd.DataFrame([{
            "Serial No.": len(st.session_state.database) + 1,  # Serial starts from 1
            "First Name": st.session_state.first_name,
            "Last Name": st.session_state.last_name,
            "Contact #": st.session_state.contact,
            "Country of Residence": st.session_state.country,
            "LinkedIn URL": st.session_state.linkedin,
            "Industry": st.session_state.industry,
            "Position": st.session_state.position,
            "Areas of Collaboration": st.session_state.collaboration,
        }])
        
        # Update the database in the background (hidden)
        st.session_state.database = pd.concat([st.session_state.database, new_entry], ignore_index=True)
        st.success("Your data has been added successfully!")

        # Reset form fields by clearing session state values
        st.session_state.first_name = ""
        st.session_state.last_name = ""
        st.session_state.contact = ""
        st.session_state.country = ""
        st.session_state.linkedin = ""
        st.session_state.industry = ""
        st.session_state.position = ""
        st.session_state.collaboration = ""

# Footer
st.markdown("---")
st.markdown("<center>A tool to facilitate interaction among PEF members by Khalid Baig</center>", unsafe_allow_html=True)
