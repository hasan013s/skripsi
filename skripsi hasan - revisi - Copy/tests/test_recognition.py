from services.face_recognition_service import FaceRecognitionService
import cv2

service = FaceRecognitionService()
img = cv2.imread("static/sample_faces/sample1.jpg")
result = service.process_frame(img)
cv2.imshow("Test Recognition", result)
cv2.waitKey(0)
cv2.destroyAllWindows()