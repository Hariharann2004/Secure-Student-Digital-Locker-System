import streamlit as st
# Explicitly import all pages at the top
import pages.share as share
from pages import login, register, dashboard, upload, files


# 1. Page Config - MUST BE FIRST
st.set_page_config(page_title="Secure Digital Locker", layout="wide")

# 2. Initialize Session State
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

def main():
    # 3. Sidebar Setup
    st.sidebar.title("🔐 Digital Vault")
    
    if st.session_state.user_id is None:
        # User is logged out
        menu = ["Login", "Register"]
        choice = st.sidebar.radio("Navigation", menu)
        
        if choice == "Login":
            login.show()
        else:
            register.show()
    else:
        # User is logged in
        st.sidebar.success(f"Logged in: {st.session_state.user_email}")
        
        menu = ["Dashboard", "Upload", "My Files","Share", "Logout"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == "Dashboard":
            dashboard.show()
        elif choice == "Upload":
            upload.show()
        elif choice == "My Files":
            files.show()
        elif choice == "Share":  # Make sure this matches exactly
            share.show()
        elif choice == "Logout":
            # Clear session and reset
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.rerun()

if __name__ == "__main__":
    main()