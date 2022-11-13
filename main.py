from flask import Flask, render_template, request
from flask_restful import Api, Resource
import mysql.connector
from datetime import datetime, timedelta
import json

app = Flask(__name__, template_folder="./html")
api = Api(app)


# starting point: show login page
# render login.html
@app.route("/")
def index():
    print("GET index.html")
    return render_template("index.html")

@app.route("/faceLogin.html")
def faceLogin():
    print("GET faceLogin.html")
    return render_template("faceLogin.html")

# @app.route("/faceLogin", methods=['POST', 'GET'])
@app.route("/faceLogin")
def faceLoginProcess():
    print("GET faceLogin")
    from login_face import check_face
    name = check_face()
    if (name=="404"):
        return json.dumps({"value":"None"})
    else:
        from update_login_info import update_login_info
        update_login_info(name)
        return json.dumps({"value":name})

@app.route("/loginRecord/<studentName>")
def loginRecord(studentName):
    print("GET loginRecord with studentName="+studentName)
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    get_uid_sql = "Select student_id from student Where student_name=%s"
    cursor.execute(get_uid_sql, [studentName])
    uid = cursor.fetchall()[0][0]

    sql = "Select * from login_record (Select Max(behaviour_id) From login_record Where student_id=%s)"
    cursor.execute(sql, [uid])
    last_login_record = cursor.fetchall()
    print(last_login_record)


@app.route("/faceRegister.html")
def faceRegister():
    print("GET faceRegister.html")
    return render_template("faceRegister.html")


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

@app.route("/homepage/<studentName>/logout")
def logout(studentName):
    print("GET logout with username="+studentName)
    time = datetime.now()
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    get_uid_sql = "Select student_id From student Where student_name=%s"
    cursor.execute(get_uid_sql, [studentName])
    uid = cursor.fetchall()[0][0]

    get_behaviour_id_sql = "Select behaviour_id, login_time From login_record Where student_id=%s and logout_time is NULL"
    cursor.execute(get_behaviour_id_sql, [uid])
    behaviour_id, login_time = cursor.fetchall()[-1]
    sql = "Update login_record Set logout_time=%s, duration=%s Where student_id=%s and behaviour_id=%s"    
    duration = str(timedelta(seconds = (time-login_time).total_seconds()))
    cursor.execute(sql, [time, duration, uid, behaviour_id])
    result = cursor.fetchall()
    print(result)
    myconn.commit()

    return json.dumps({"result": "Log out successfully"})


if __name__ == "__main__":
    app.run(debug=True)
