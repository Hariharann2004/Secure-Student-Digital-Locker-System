import streamlit as st
import requests

def show():
    st.title("📂 File Explorer")

    if not st.session_state.user_id:
        st.warning("Please login to view your files.")
        return

    user_id = st.session_state.user_id

    # Create Tabs for a organized UI
    tab1, tab2 = st.tabs(["My Personal Vault", "Shared With Me"])

    with tab1:
        st.subheader("Your Encrypted Files")
        render_file_list(f"http://localhost:5000/files/list/{user_id}", "Your vault is empty. Upload a file to get started!", user_id)

    with tab2:
        st.subheader("Files Shared by Others")
        # This calls the 'shared' endpoint we discussed for the multi-user flow
        render_file_list(f"http://localhost:5000/files/shared/{user_id}", "No one has shared any files with you yet.", user_id)

def render_file_list(api_url, empty_message, user_id):
    """Helper function to render file rows for both tabs."""
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            files_list = response.json()
            
            if not files_list:
                st.info(empty_message)
            else:
                for f in files_list:
                    with st.container():
                        st.markdown("---")
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.subheader(f"📄 {f['file_name']}")
                            # Safe date extraction using your 'upload_time' column
                            upload_date = f.get('upload_time', 'N/A')[:10]
                            #st.caption(f"Category: {f['category']} | Date: {upload_date}")
                            # Inside your loop for shared files
                            st.caption(f"Category: {f['category']} | Sent by: {f.get('owner_email', 'Shared User')}")
                        
                        with col2:
                            # Unique key per button to avoid Streamlit DuplicateKeyError
                            if st.button("🔓 Prepare", key=f"btn_{f['id']}"):
                                prepare_and_show_download(f['id'], f['file_name'], user_id)
        else:
            st.error(f"Backend Error: {response.status_code}. Verify RLS policies.")
            
    except Exception as e:
        st.error(f"Connection error: {e}")

def prepare_and_show_download(file_id, file_name, user_id):
    """Hits the Flask decryption endpoint and generates the download button."""
    url = f"http://localhost:5000/files/download/{file_id}?user_id={user_id}"
    
    with st.spinner("Decrypting with AES-256..."):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                st.success("File ready!")
                st.download_button(
                    label="💾 Download Decrypted File",
                    data=res.content,
                    file_name=file_name,
                    mime="application/octet-stream",
                    key=f"dl_ready_{file_id}"
                )
            else:
                error_msg = res.json().get('error', 'Decryption failed.')
                st.error(f"Error: {error_msg}")
        except Exception as e:
            st.error(f"Request failed: {e}")