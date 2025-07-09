import face_recognition
import os

def encode_faces_from_dir(directory):
    encodings = []
    names = []
    for file in os.listdir(directory):
        if file.endswith(".jpg") or file.endswith(".png"):
            path = os.path.join(directory, file)
            img = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(img)
            if encoding:
                encodings.append(encoding[0])
                names.append(os.path.splitext(file)[0])
    return encodings, names

def encode_face(frame, location):
    rgb_frame = frame[:, :, ::-1]
    encodings = face_recognition.face_encodings(rgb_frame, [location])
    return encodings[0] if encodings else None