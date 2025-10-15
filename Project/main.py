import sys
import cv2
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

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(60)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        h, w, ch = image.shape
        bpl = ch * w
        qt_image = QImage(image.data, w, h, bpl, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qt_image)

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



