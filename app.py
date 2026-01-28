import streamlit as st
import subprocess
import sys
import os
import pandas as pd
from glob import glob

# ---------------------- CONFIG ----------------------
DATA_DIR = "data"
ATTENDANCE_DIR = "Attendance"
# ----------------------------------------------------

st.set_page_config(page_title="Face Attendance System", layout="centered")

st.title("🎓 Face Recognition Attendance System")
st.markdown("---")

st.markdown("""
### Features
- Identify the face
- Punch-In attendance
- Punch-Out attendance
- View Attendance Sheet
""")
st.markdown("---")

# ---------------------- BUTTONS ----------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("📸 Add New Face"):
        st.info("Opening camera to collect face data...")
        subprocess.Popen([sys.executable, "add_faces.py"])

with col2:
    if st.button("🕒 Start Attendance (IN / OUT)"):
        st.info("Starting face recognition & attendance...")
        subprocess.Popen([sys.executable, "test.py"])

st.markdown("---")

# ---------------------- VIEW ATTENDANCE ----------------------
st.header("📄 Attendance Sheet")

# List all attendance CSV files
csv_files = sorted(glob(os.path.join(ATTENDANCE_DIR, "Attendance_*.csv")), reverse=True)

if csv_files:
    st.subheader(f"Latest Attendance File: {os.path.basename(csv_files[0])}")
    try:
        df = pd.read_csv(csv_files[0], on_bad_lines="skip")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading latest file: {e}")

    st.markdown("---")
    st.subheader("Or select a different attendance file:")
    selected_file = st.selectbox("Select file", csv_files, format_func=lambda x: os.path.basename(x))
    if selected_file:
        try:
            df_sel = pd.read_csv(selected_file, on_bad_lines="skip")
            st.dataframe(df_sel)
        except Exception as e:
            st.error(f"Error reading selected file: {e}")
else:
    st.info("No attendance records found yet.")

# ---------------------- INSTRUCTIONS ----------------------
st.markdown("---")
st.markdown("### Instructions")
st.markdown("""
1. Click **Add New Face**  
   - Enter name in terminal  
   - Look at camera until samples complete  

2. Click **Start Attendance**
   - Press **i** → Punch-In  
   - Press **o** → Punch-Out  
   - Press **q** → Quit  

3. Attendance CSV is saved automatically in `Attendance` folder
""")

st.success("✅ System ready for use on localhost")
