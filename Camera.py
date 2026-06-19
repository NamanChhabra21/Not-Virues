import cv2
import time
import threading

class OpenCamera:
    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        self.success = False
        self.running = False

        if self.cap.isOpened():
            self.success = True
            self.running = True


    def show(self):

        cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while self.running:
            ret, frame = self.cap.read()

            if not ret:
                break

            cv2.imshow("Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False

time.sleep(4)