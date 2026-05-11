import streamlit as st
import requests

def show_logs():
    st.subheader("🕒 Recent Activity")
    user_id = st.session_state.user_id
    
    try:
        response = requests.get(f"http://localhost:5000/logs/{user_id}")
        if response.status_code == 200:
            logs = response.json()
            if logs:
                for log in logs[:5]:
                    # UPDATED: Use log['timestamp'] instead of created_at
                    time_data = log.get('timestamp', 'Unknown Time')
                    time_str = time_data.replace("T", " ")[:16]
                    
                    st.write(f"✅ {time_str} | **{log['action']}**")
                    if log.get('details'):
                        st.caption(f"Details: {log['details']}")
            else:
                st.info("No recent activity found.")
        else:
            st.write("Unable to fetch activity logs. Check RLS policies.")
    except Exception as e:
        st.write(f"Could not load activity logs: {e}")

def show():
    st.title(f"👋 Welcome to Your Secure Vault")
    st.write(f"Logged in as: **{st.session_state.user_email}**")
    
    st.markdown("---")
    
    # 1. Quick Stats
    col1, col2, col3 = st.columns(3)
    
    try:
        user_id = st.session_state.user_id
        response = requests.get(f"http://localhost:5000/files/list/{user_id}")
        
        if response.status_code == 200:
            files = response.json()
            total_files = len(files)
            
            # Count by category
            categories = [f['category'] for f in files]
            resumes = categories.count("RESUME")
            certs = categories.count("CERTIFICATE")

            col1.metric("Total Files", total_files)
            col2.metric("Resumes", resumes)
            col3.metric("Certificates", certs)
        else:
            st.error("Could not load stats.")
    except:
        st.warning("Backend not reachable for stats.")

    st.markdown("---")

    # 2. Activity Feed (Your New Section)
    show_logs()

    st.markdown("---")

    # 3. Quick Actions
    st.subheader("Quick Actions")
    q_col1, q_col2 = st.columns(2)
    
    if q_col1.button("📤 Upload New File", use_container_width=True):
        st.info("Select 'Upload' from the sidebar menu!")
        
    if q_col2.button("📂 View All Files", use_container_width=True):
        st.info("Select 'My Files' from the sidebar menu!")

    # 4. Security Tip
    st.info("🛡️ **Security Note:** Your files are encrypted using AES-256 before they ever reach the cloud.")