import cv2
from services.face_recognition_service import FaceRecognitionService

def main():
    # Inisialisasi layanan pengenalan wajah
    service = FaceRecognitionService()

    # Buka kamera default (0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Tidak dapat membuka kamera.")
        return

    print("✅ Kamera berhasil dibuka. Tekan 'q' untuk keluar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Gagal membaca frame dari kamera.")
            break

        # Proses frame untuk pendeteksian wajah
        frame = service.process_frame(frame)

        # Tampilkan hasil ke layar
        cv2.imshow("Real-Time Absensi Wajah", frame)

        # Keluar jika pengguna menekan tombol 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Bersihkan dan tutup semua jendela
    cap.release()
    cv2.destroyAllWindows()
    print("📷 Kamera dimatikan. Program selesai.")

if __name__ == "__main__":
    main()
