import streamlit as st
import requests

def show():
    st.title("📤 Upload Secure File")
    
    if not st.session_state.user_id:
        st.warning("Please login first.")
        return

    # Category dropdown
    categories = ["CERTIFICATE", "RESUME", "NOTES", "PHOTOS", "PROJECT"]
    category = st.selectbox("Select File Category", categories)
    
    uploaded_file = st.file_uploader("Choose a file to encrypt and upload")

    if st.button("Encrypt & Upload"):
        if uploaded_file is not None:
            with st.spinner("Encrypting and uploading..."):
                # Prepare data
                files_payload = {'file': (uploaded_file.name, uploaded_file.getvalue())}
                data_payload = {
                    'user_id': st.session_state.user_id,
                    'category': category
                }

                try:
                    response = requests.post("http://localhost:5000/files/upload", files=files_payload, data=data_payload)
                    
                    if response.status_code == 200:
                        st.success(f"Successfully uploaded {uploaded_file.name} to {category}!")
                        st.balloons()
                    else:
                        error_detail = response.json().get('error', 'Unknown Error')
                        st.error(f"Upload failed: {error_detail}")
                except Exception as e:
                    st.error(f"Connection Error: {e}. Is the Flask backend running?")
        else:
            st.error("Please select a file first.")