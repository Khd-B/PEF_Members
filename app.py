import streamlit as st
import pandas as pd

# Initialize the database in session state
if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame(columns=[
        "First Name", "Last Name", "Contact #", "Country of Residence", 
        "LinkedIn URL", "Industry", "Position", "Areas of Collaboration"
    ])

st.title("Professional Collaboration Platform")

# Input Form
with st.form("user_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    contact = st.text_input("Contact #")
    country = st.text_input("Country of Residence")
    linkedin = st.text_input("LinkedIn URL")
    industry = st.text_input("Industry")
    position = st.text_input("Position")
    collaboration = st.text_area("Areas of Collaboration")
    submitted = st.form_submit_button("Submit")

if submitted:
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

st.header("Database")
st.dataframe(st.session_state.database)

if st.button("Save Database"):
    st.session_state.database.to_csv("database.csv", index=False)
    st.success("Database saved to database.csv!")

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
