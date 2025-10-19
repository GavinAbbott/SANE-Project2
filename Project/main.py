import sys
print(sys.path)
import cv2
import time
from fer import FER
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class WebcamApp(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('Main.ui',self)


        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open video camera")
            return

        self.fpsFrameCount = 0
        self.fpsStartTime = time.time()

        self.detector = FER(mtcnn=True)
        self.emotionTimer = time.time()
        self.lastDetectionResult = []



        self.emotionTimer = time.time()
        self.lastDetectionResult = []


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(0)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        if self.mirrorbox.isChecked():
            frame = cv2.flip(frame,1)




        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        h, w, ch = image.shape
        bpl = ch * w
        qt_image = QImage(image.data, w, h, bpl, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qt_image)

        self.fpsFrameCount += 1

        currentTime = time.time()

        elapsedTime = currentTime - self.fpsStartTime

        if currentTime - self.emotionTimer >= 2:
            self.lastDetectionResult = self.detector.detect_emotions(frame)
            self.emotionTimer = currentTime

        if self.lastDetectionResult:
            firstFace = self.lastDetectionResult[0]
            emotions = firstFace['emotions']

            happyScore = emotions['happy'] * 100
            sadScore = emotions['sad'] * 100
            angryScore = emotions['angry'] * 100
            neutralScore = emotions['neutral'] * 100

            self.happyLabel.setText(f"Happy: {happyScore: .1f}%")
            self.sadLabel.setText(f"Sad: {sadScore: .1f}%")
            self.angryLabel.setText(f"Angry: {angryScore: .1f}%")
            self.neutralLabel.setText(f"Neutral: {neutralScore: .1f}%" )
        else:
            self.happyLabel.setText("Happy: ?%")
            self.sadLabel.setText("Sad: ?%")
            self.angryLabel.setText("Angry: ?%" )
            self.neutralLabel.setText("Neutral: ?%" )





        if elapsedTime >= 1:
            fps = self.fpsFrameCount/ elapsedTime
            self.fpsLabel.setText(f"FPS: {fps: .2f}")

            self.fpsFrameCount = 0
            self.fpsStartTime = currentTime



        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(),Qt.KeepAspectRatioByExpanding,Qt.SmoothTransformation))

    def closeEvent(self, event):
        print("done with camera")
        self.cap.release()
        super().closeEvent(event)





if __name__=='__main__':
    app = QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec_())



