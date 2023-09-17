import cv2
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class NfeScanner(QMainWindow):
    qr_code_detected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Code Scanner")
        self.setFixedSize(640, 480)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.video_label)

        self.video_capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            # Convert the frame to RGB format
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create a QImage from the RGB image
            image = QImage(
                rgb_image.data,
                rgb_image.shape[1],
                rgb_image.shape[0],
                QImage.Format.Format_RGB888
            )

            # Create a QPixmap from the QImage
            pixmap = QPixmap.fromImage(image)

            # Scale the pixmap to fit the label
            scaled_pixmap = pixmap.scaled(
                self.video_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # Set the pixmap to the label
            self.video_label.setPixmap(scaled_pixmap)

            # Call the QR code detection and decoding function
            data = self.detect_qr_code(frame)

            if data:
                self.qr_code_detected.emit(data)
                QApplication.quit()

    def detect_qr_code(self, frame):
        qr_code_detector = cv2.QRCodeDetector()
        data, points, _ = qr_code_detector.detectAndDecode(frame)

        if data:
            print("QR Code Detected")
            print(f"URL: {data}")
            return data

        return False

    def closeEvent(self, event):
        self.video_capture.release()
        event.accept()
