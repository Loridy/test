import cv2
import pickle
import pyttsx3
import mysql.connector
import time

def check_face():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("train.yml")

    labels = {"person_name": 1}
    with open("labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}
    # create text to speech
    engine = pyttsx3.init()
    rate = engine.getProperty("rate")
    engine.setProperty("rate", 175)
    # Define camera and detect face
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    start = time.time()
    while (time.time()-start<3):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    
        for (x, y, w, h) in faces:
            # print(x, w, y, h)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            # predict the id and confidence for faces
            id_, conf = recognizer.predict(roi_gray)
            
            # if face is recogized
            gui_confidence = 0.5
            # print(id_
            if conf >= gui_confidence:
                name = labels[id_]
                name = name.replace("_", " ")
                # connect database
                myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
                cursor = myconn.cursor()
                sql = "SELECT student_name from student WHERE student_name=%s"
                cursor.execute(sql, [name])
                result = cursor.fetchall()
                myconn.commit()
                print(name)
                print(result)
                if (result==[]):
                    return "404"
                else:
                    # student found in database
                    return name
            else:
                print("Face not recoginized")
    # timeout
    return "404"

