import cv2
import pickle
import numpy as np
import os

# ---------------------- CONFIG ----------------------
DATA_DIR = "data"
FACE_SIZE = (50, 50)
MAX_SAMPLES = 100
CAMERA_INDEX = 0
# ----------------------------------------------------

os.makedirs(DATA_DIR, exist_ok=True)

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if face_cascade.empty():
    raise IOError("Haarcascade file not loaded")

# Open camera
video = cv2.VideoCapture(CAMERA_INDEX)
if not video.isOpened():
    raise IOError("Cannot access camera")

name = input("Enter Your Name: ")

faces_data = []
frame_count = 0

print("📸 Collecting face data... Press 'q' to quit")

# ---------------------- CAPTURE LOOP ----------------------
while True:
    ret, frame = video.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, FACE_SIZE)

        if len(faces_data) < MAX_SAMPLES and frame_count % 10 == 0:
            faces_data.append(face_img)

        frame_count += 1

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Samples: {len(faces_data)}/{MAX_SAMPLES}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Capture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or len(faces_data) >= MAX_SAMPLES:
        break

# ---------------------- CLEANUP ----------------------
video.release()
cv2.destroyAllWindows()

# ---------------------- DATA PROCESSING ----------------------
faces_data = np.asarray(faces_data)

if len(faces_data) == 0:
    raise ValueError("No faces captured. Try again.")

faces_data = faces_data.reshape(len(faces_data), -1)

# ---------------------- SAVE NAMES ----------------------
names_path = os.path.join(DATA_DIR, "names.pkl")

if os.path.exists(names_path):
    with open(names_path, "rb") as f:
        names = pickle.load(f)
else:
    names = []

names.extend([name] * len(faces_data))

with open(names_path, "wb") as f:
    pickle.dump(names, f)

# ---------------------- SAVE FACE DATA ----------------------
faces_path = os.path.join(DATA_DIR, "faces_data.pkl")

if os.path.exists(faces_path):
    with open(faces_path, "rb") as f:
        existing_faces = pickle.load(f)
    faces_data = np.append(existing_faces, faces_data, axis=0)

with open(faces_path, "wb") as f:
    pickle.dump(faces_data, f)

print(f"✅ Saved {len(faces_data)} face samples for {name}")
