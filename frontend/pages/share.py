import streamlit as st
import requests

def show():
    st.title("🤝 Share Secure Access")
    st.write("Grant another user permission to decrypt your files.")

    if not st.session_state.user_id:
        st.warning("Please login first.")
        return

    user_id = st.session_state.user_id

    try:
        # 1. Fetch the user's files to populate the dropdown
        response = requests.get(f"http://localhost:5000/files/list/{user_id}")
        
        if response.status_code == 200:
            files = response.json()
            
            if not files:
                st.info("You don't have any files to share yet. Upload something first!")
                return

            # Create a dictionary for the dropdown
            file_options = {f"{f['file_name']} ({f['category']})": f['id'] for f in files}
            
            # UI Components
            selected_label = st.selectbox("Select a file to share", list(file_options.keys()))
            recipient_email = st.text_input("Enter Recipient's Email")
            
            if st.button("Grant Access", use_container_width=True):
                if recipient_email:
                    file_id = file_options[selected_label]
                    
                    payload = {
                        "file_id": file_id,
                        "email": recipient_email,
                        "owner_id": user_id
                    }
                    
                    with st.spinner("Updating permissions..."):
                        share_res = requests.post("http://localhost:5000/share/add", json=payload)
                        
                        if share_res.status_code == 200:
                            st.success(f"Successfully shared with {recipient_email}!")
                            st.balloons()
                        else:
                            error_msg = share_res.json().get('error', 'Unknown Error')
                            st.error(f"Sharing failed: {error_msg}")
                else:
                    st.error("Please enter a recipient email address.")
        else:
            st.error("Failed to fetch your file list from the server.")
            
    except Exception as e:
        st.error(f"Connection Error: {e}")