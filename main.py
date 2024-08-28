import cv2
from pyzbar.pyzbar import decode
import requests
import datetime

# URL endpoint untuk mengirim data ke server PHP
url = "http://localhost/absensi.php"  # Ganti dengan URL endpoint yang sesuai

# Mulai menggunakan kamera webcam untuk video capture
video_capture = cv2.VideoCapture(0)  # '0' menunjukkan webcam default

while True:
    # Membaca frame dari video capture
    ret, frame = video_capture.read()

    # Decode objek QR code dari frame yang telah dibaca
    decoded_objects = decode(frame)
    qr_detected = False  # Flag untuk memeriksa apakah QR code terdeteksi

    for obj in decoded_objects:
        qr_detected = True  # Jika QR code terdeteksi, set flag ke True

        # Ekstrak data dari QR code yang terdeteksi
        qr_data = obj.data.decode('utf-8')

        # Gambar kotak di sekitar QR code yang terdeteksi
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Tampilkan label di atas QR code yang terdeteksi
        label = "QR Detected"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Siapkan data yang akan dikirim ke server
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {'qr_data': qr_data, 'timestamp': timestamp}

        # Kirim data ke server menggunakan HTTP POST request
        response = requests.post(url, data=data)
        print(f"Data sent: {data}")  # Output data yang dikirim ke terminal

    if not qr_detected:
        # Tampilkan pesan jika tidak ada QR code yang terdeteksi
        label = "Kode QR Tidak Terdeteksi, Coba Lagi."
        cv2.putText(frame, label, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Tampilkan frame yang telah diproses ke layar
    cv2.imshow('Kode QR Terdeteksi', frame)

    # Berhenti jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan resource video capture dan menutup semua jendela OpenCV
video_capture.release()
cv2.destroyAllWindows()
