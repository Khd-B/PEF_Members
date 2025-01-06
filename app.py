import streamlit as st
import pandas as pd
import pycountry

# Initialize database as a DataFrame
if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame(columns=[
        "First Name", "Last Name", "Contact #", "Country of Residence",
        "LinkedIn URL", "Industry", "Position", "Areas of Collaboration"
    ])

# Generate country list and country_codes dictionary using pycountry
country_list = [country.name for country in pycountry.countries if hasattr(country, 'calling_codes') and country.calling_codes]
country_codes = {country.name: f"+{country.calling_codes[0]}" for country in pycountry.countries if hasattr(country, 'calling_codes') and country.calling_codes}


st.title("Professional Collaboration Platform")

# Input Form
with st.form("user_form"):
    first_name = st.text_input("First Name", key="first_name")
    last_name = st.text_input("Last Name", key="last_name")

    # Country and Contact # with automation
    country = st.selectbox("Country of Residence", country_list, key="country")
    contact = st.text_input("Contact #", value=country_codes.get(country, ""), key="contact")

    linkedin = st.text_input("LinkedIn URL", key="linkedin")
    industry = st.text_input("Industry", key="industry")
    position = st.text_input("Position", key="position")
    collaboration = st.text_area("Areas of Collaboration", key="collaboration")
    submitted = st.form_submit_button("Submit")

# Handle Form Submission
if submitted:
    # Add data to the session's database
    new_entry = {
        "First Name": first_name,
        "Last Name": last_name,
        "Contact #": contact,
        "Country of Residence": country,
        "LinkedIn URL": linkedin,
        "Industry": industry,
        "Position": position,
        "Areas of Collaboration": collaboration,
    }
    st.session_state.database = pd.concat([st.session_state.database, pd.DataFrame([new_entry])], ignore_index=True)
    st.success("Your data has been added successfully!")

    # Clear input fields using session state
    for key in ["first_name", "last_name", "contact", "linkedin", "industry", "position", "collaboration"]:
        st.session_state[key] = ""
    st.session_state.country = country_list[0]  # Reset country to default

# Display database
st.header("Database")
st.dataframe(st.session_state.database)

# Save data to CSV
if st.button("Save Database"):
    st.session_state.database.to_csv("database.csv", index=False)
    st.success("Database saved to database.csv!")

# Search functionality
st.header("Search Database")
search_term = st.text_input("Search by Name, Industry, or Collaboration Area")

if search_term:
    results = st.session_state.database[
        st.session_state.database.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)
    ]
    if not results.empty:
        st.dataframe(results)
    else:
        st.warning("No results found.")
