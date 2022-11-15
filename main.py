from flask import Flask, render_template, request
from flask_restful import Api, Resource
import mysql.connector
from datetime import datetime, timedelta
import json

app = Flask(__name__, template_folder="./html")


# starting point: show login page
# render login.html
@app.route("/")
def index():
    print("GET index.html")
    return render_template("index.html")


# render faceLogin.html
# may use "/faceLogin" to login to the homepage
@app.route("/faceLogin.html")
def faceLogin():
    print("GET faceLogin.html")
    return render_template("faceLogin.html")


# "/faceLogoin" api is used to check if user is registed
# it will return a json data {"value": name} if recognized; {"value":"Already login"}; otherwise {"value": "None"}
# the backend will automatically open the camera to check user's face(do not have a popup window)
@app.route("/faceLogin")
def faceLoginProcess():
    print("GET faceLogin")
    from login_face import check_face
    name = check_face()
    if (name=="404"):
        return json.dumps({"value":"None"}) # face not recognized
    else:
        myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
        cursor = myconn.cursor()
        sql = "Select student_name from student s, login_record l Where s.student_id=l.student_id and logout_time is NULL;"
        # sql = "Select student_name from student"
        cursor.execute(sql)
        result = cursor.fetchall()
        names = [_[0].lower() for _ in result]
        if (name.lower() in names):
            return json.dumps({"value": "Already Login"}) # student already login
        from update_login_info import update_login_info
        update_login_info(name)
        return json.dumps({"value":name})


# render faceRegister.html
# may contain content that require user registration info (studentName, studentId, department, email)
@app.route("/faceRegister.html")
def faceRegister():
    print("GET faceRegister.html")
    return render_template("faceRegister.html")


# used for user registration
# need (studentName, studentId, department, email) information in JSON
# after register, store student face info(automatically open camera; do not have popup window)
# will return "OK" if register successfully
@app.route("/faceRegister", methods=['POST', 'GET'])
def faceRegisterProcess():
    content = request.get_json()
    studentName = content["studentName"]
    studentId = content["studentId"]
    department = content["department"]
    email = content["email"]
    print("GET faceRegisterProcess with studentName="+studentName)
    
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    sql = "INSERT INTO `student` (`student_id`, `department`,`email`,`student_name`,`moodle`) VALUES(%s, %s, %s, %s, %s)"
    cursor.execute(sql, [studentId, department, email, studentName, "N/A"])
    result = cursor.fetchall()
    myconn.commit()

    from face_capture import face_capture
    face_capture(studentName)
    from train import train
    train()
    return "OK"

@app.route("/homepage/<studentName>")
def homepage(studentName):
    pass

# Under user's own homepage
# User should manually logout in order to store the logout time
# Usually will return {"result": "Log out successfully"}
# will return {"result": "Already logout"} if you test wrongly (eg. logout when user hasn't login)
@app.route("/homepage/<studentName>/logout")
def logout(studentName):
    print("GET logout with username="+studentName)
    time = datetime.now()
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    get_uid_sql = "Select student_id From student Where student_name=%s"
    cursor.execute(get_uid_sql, [studentName])
    result = cursor.fetchall()
    uid = result[0][0]

    get_behaviour_id_sql = "Select behaviour_id, login_time From login_record Where student_id=%s and logout_time is NULL"
    cursor.execute(get_behaviour_id_sql, [uid])
    result = cursor.fetchall()
    print(result)
    if len(result)==0:
        return json.dumps({"result": "Already logout"})
    behaviour_id, login_time = result[-1]
    sql = "Update login_record Set logout_time=%s, duration=%s Where student_id=%s and behaviour_id=%s"    
    duration = str(timedelta(seconds = (time-login_time).total_seconds()))
    cursor.execute(sql, [time, duration, uid, behaviour_id])
    result = cursor.fetchall()
    myconn.commit()

    return json.dumps({"result": "Log out successfully"})


# may under loginRecord page
# used to show user loginRecord
@app.route("/loginRecord/<studentName>")
def loginRecord(studentName):
    print("GET loginRecord with studentName="+studentName)
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    get_uid_sql = "Select student_id from student Where student_name=%s"
    cursor.execute(get_uid_sql, [studentName])
    uid = cursor.fetchall()[0][0]

    sql = "Select * From login_record Where behaviour_id =(Select Max(behaviour_id) From login_record Where student_id=%s)"
    cursor.execute(sql, [uid])
    result = cursor.fetchall()
    last_login_record = result[0]
    studentID, total_login_times, last_login_time, last_logout_time, duration = last_login_record
    last_login_time = last_login_time.strftime("%H:%M:%S")
    last_logout_time = last_logout_time.strftime("%H:%M:%S")
    duration = str(duration)
    # print(last_login_time, last_logout_time, str(duration))
    # print(type(duration))
    return json.dumps({"studentID":studentID, "total_login_times":total_login_times, "last_login_time":last_login_time, "last_logout_time":last_logout_time, "duration":duration})

if __name__ == "__main__":
    app.run(debug=True)
