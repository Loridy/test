import cv2
import os

def face_capture(studentName):
    NUM_IMGS = 50
    count = 1
    video_capture = cv2.VideoCapture(0)
    studentName = studentName.replace(" ", "_")
    if not os.path.exists("data/{}".format(studentName.upper())):
        os.mkdir("data/{}".format(studentName.upper()))

    while count <= NUM_IMGS:
        ret, frame = video_capture.read()
        cv2.imshow('webcam', frame)
        cv2.imwrite(
            "data/{}/{}{:03d}.jpg".format(studentName.upper(), studentName.upper(), count), frame)
        count += 1
        cv2.waitKey(10)
    video_capture.release()
    cv2.destroyAllWindows()

