import streamlit as st
import requests

def show():
    st.title("Create an Account")
    
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        try:
            # Connect to Flask Backend
            response = requests.post("http://localhost:5000/auth/register", json={
                "name": name,
                "email": email,
                "password": password
            })
            
            if response.status_code == 201:
                st.success("Registration successful! Please login from the sidebar.")
            else:
                error_msg = response.json().get('error', 'Registration failed')
                st.error(f"Error: {error_msg}")
        except Exception as e:
            st.error(f"Could not connect to backend: {e}")