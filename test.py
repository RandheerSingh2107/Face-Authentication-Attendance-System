from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

# ---------------------- CONFIG ----------------------
DATA_DIR = "data"
ATTENDANCE_DIR = "Attendance"
FACE_SIZE = (50, 50)
CAMERA_INDEX = 0
# ----------------------------------------------------

os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# ---------------------- TEXT TO SPEECH ----------------------
def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# ---------------------- LOAD FACE DETECTOR ----------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if face_cascade.empty():
    raise IOError("Haarcascade file not loaded")

# ---------------------- CAMERA ----------------------
video = cv2.VideoCapture(CAMERA_INDEX)
if not video.isOpened():
    raise IOError("Cannot open camera")

# ---------------------- LOAD DATA ----------------------
with open(os.path.join(DATA_DIR, "names.pkl"), "rb") as f:
    LABELS = pickle.load(f)

with open(os.path.join(DATA_DIR, "faces_data.pkl"), "rb") as f:
    FACES = pickle.load(f)

# Safety check
if len(FACES) != len(LABELS):
    raise ValueError(f"Mismatch: Faces={len(FACES)}, Labels={len(LABELS)}")

print("✅ Faces loaded:", FACES.shape)

# ---------------------- TRAIN MODEL ----------------------
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# ---------------------- UI ----------------------
imgBackground = cv2.imread("background.png")
COL_NAMES = ["NAME", "DATE", "TIME", "STATUS"]

print("🎥 System Ready | i = Punch-In | o = Punch-Out | q = Quit")

# ---------------------- MAIN LOOP ----------------------
while True:
    ret, frame = video.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    recognized_names = []

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, FACE_SIZE).flatten().reshape(1, -1)

        name_pred = knn.predict(face_img)[0]
        recognized_names.append(name_pred)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(
            frame,
            name_pred,
            (x, y-10),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 255, 255),
            2
        )

    # Take the **first recognized face** for punch
    current_name = recognized_names[0] if recognized_names else None

    # Display frame
    if imgBackground is not None:
        imgBackground[162:162+480, 55:55+640] = frame
        cv2.imshow("Attendance System", imgBackground)
    else:
        cv2.imshow("Attendance System", frame)

    key = cv2.waitKey(10) & 0xFF  # slightly longer wait to ensure key capture

    # ---------------------- PUNCH LOGIC ----------------------
    if current_name and key in [ord('i'), ord('o')]:
        status = "IN" if key == ord('i') else "OUT"

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

        file_path = os.path.join(
            ATTENDANCE_DIR,
            f"Attendance_{date}.csv"
        )

        print(f"Attempting punch for {current_name} | {status} | {timestamp}")
        print(f"CSV file: {os.path.abspath(file_path)}")

        file_exists = os.path.isfile(file_path)
        already_punched = False

        # Check if already punched
        if file_exists:
            with open(file_path, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

                for row in rows[1:]:
                    if len(row) < 4:
                        continue
                    if row[0] == current_name and row[3] == status:
                        already_punched = True
                        break

        if already_punched:
            speak(f"Already punched {status}")
            print(f"⚠ Already punched {status}")
        else:
            # Write to CSV
            with open(file_path, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(COL_NAMES)
                writer.writerow([current_name, date, timestamp, status])

            speak(f"Punch {status} recorded")
            print(f"📝 {current_name} | {status} | {timestamp}")
            time.sleep(1)  # short delay to avoid duplicate punches

    if key == ord('q'):
        print("Quitting...")
        break

# ---------------------- CLEANUP ----------------------
video.release()
cv2.destroyAllWindows()
