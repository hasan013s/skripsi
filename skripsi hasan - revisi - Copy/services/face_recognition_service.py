# services/face_recognition_service.py

import cv2
from deepface import DeepFace
from utils.face_detector import detect_face
from utils.attendance_logger import log_attendance
from utils.sound_player import speak
import mediapipe as mp
import os

class FaceRecognitionService:
    def __init__(self):
        print("FaceRecognitionService initialized")

        # Inisialisasi untuk deteksi kedipan (liveness)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)

    def is_blinking(self, frame):
        # Fungsi untuk mendeteksi kedipan mata
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return False

        for face_landmarks in results.multi_face_landmarks:
            # EAR (Eye Aspect Ratio) sederhana antara landmark 159 dan 145
            left_eye_distance = abs(face_landmarks.landmark[159].y - face_landmarks.landmark[145].y)
            if left_eye_distance < 0.015:  # Threshold untuk kedipan (tweak sesuai kamera)
                return True
        return False

    def process_frame(self, frame):
        face_img, face_coords = detect_face(frame)
        if face_img is not None:

            # Deteksi kedipan (jika tidak kedip, anggap ini foto dan tolak)
            if not self.is_blinking(frame):
                cv2.putText(frame, "Silahkan kedipkan mata", (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                return frame  # Jangan lanjut

            try:
                result = DeepFace.find(img_path=face_img, db_path="static/sample_faces", enforce_detection=False)

                if len(result) > 0 and len(result[0]) > 0:
                    identity = result[0]["identity"][0]
                    name = os.path.basename(identity).split(".")[0]

                    log_attendance(name)
                    speak("Absen Sukses")

                    x, y, w, h = face_coords
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    speak("Absen gagal, silahkan daftar terlbih dahulu")
            except Exception as e:
                print("Recognition error:", e)
                speak("Terjadi kesalahan dalam sistem")

        return frame
