import streamlit as st
import requests

def show():
    st.title("Login to your Locker")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Connect to your Flask Backend
        try:
            response = requests.post("http://localhost:5000/auth/login", json={
                "email": email,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.user_id = data['user_id']
                st.session_state.user_email = data['email']
                st.success("Welcome back!")
                st.rerun()
            else:
                st.error("Invalid email or password.")
        except Exception as e:
            st.error(f"Could not connect to backend: {e}")