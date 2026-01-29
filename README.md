# 🎓 Face Authentication Attendance System

A Python-based **Face Recognition Attendance System** that uses computer vision and machine learning to automatically mark attendance using facial recognition. The system supports **Punch-In** and **Punch-Out**, stores attendance in CSV files, and provides a **Streamlit web interface** to manage and view attendance records.

---

## 🚀 Features

- 📸 Capture and register new faces using webcam  
- 🧠 Face recognition using KNN (K-Nearest Neighbors)  
- 🕒 Punch-In / Punch-Out attendance system  
- 📄 Attendance stored automatically in CSV files  
- 🔊 Voice feedback using Text-to-Speech  
- 🌐 Streamlit web app to:
  - Add new users
  - Start attendance system
  - View attendance sheets  

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV**
- **Scikit-learn**
- **NumPy**
- **Pandas**
- **Streamlit**
- **Haar Cascade Classifier**
- **Windows Text-to-Speech (SAPI)**

---
Face-Authentication-Attendance-System/

├── app.py # Streamlit dashboard
├── add_faces.py # Face data collection
├── test.py # Face recognition & attendance


├── data/
 ├── faces_data.pkl
 └── names.pkl

├── Attendance/
 └── Attendance_DD-MM-YYYY.csv

└── README.md

2️⃣ Add a New Face
python add_faces.py
Enter your name

Look at the camera until face samples are collected

3️⃣ Start Attendance System
python test.py


Controls:

Press i → Punch-In

Press o → Punch-Out

Press q → Quit

Attendance will be saved in the Attendance folder.

4️⃣ Run Streamlit Dashboard
streamlit run app.py


or (if Streamlit command not recognized):

python -m streamlit run app.py

📊 Attendance Output Format

CSV columns:

NAME | DATE | TIME | STATUS


Example:

Randheer Singh, 15-09-2024, 09:10:05, IN
Randheer Singh, 15-09-2024, 17:30:12, OUT

⚠️ Notes

Ensure good lighting for accurate face detection

OpenCV window must be focused when pressing keys

Close CSV files before running the program (Excel may lock them)

👨‍💻 Author

Randheer Singh
🎯 Python | Computer Vision | Machine Learning











