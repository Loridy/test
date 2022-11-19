from flask import Flask, render_template, request, send_file
from flask_restful import Api, Resource
import mysql.connector
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__, template_folder="./html")
api = Api(app)

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
    moodle = content["moodle"]
    print("GET faceRegisterProcess with studentName="+studentName)
    
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    sql = "INSERT INTO `student` (`student_id`, `department`,`email`,`student_name`,`moodle`) VALUES(%s, %s, %s, %s, %s)"
    cursor.execute(sql, [studentId, department, email, studentName, moodle])
    result = cursor.fetchall()
    myconn.commit()

    from face_capture import face_capture
    face_capture(studentName)
    from train import train
    train()
    return "OK"

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

    sql = "Select * From login_record Where behaviour_id =(Select Max(behaviour_id) From login_record Where student_id=%s and logout_time is not NULL)"
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

@app.route("/image/logo")
def getLogo():
    path = os.path.abspath(os.getcwd())+"/src/MyClass.png"
    return send_file(path, as_attachment=True)

@app.route("/image/logout")
def getLogout():
    path = os.path.abspath(os.getcwd())+"/src/logout.png"
    return send_file(path, as_attachment=True)
################################################################################################################
################################################################################################################
#################################################### PART TWO ##################################################
################################################################################################################
################################################################################################################

### shcedule page ###
@app.route("/schedule/<studentName>")
###get information and present in schedule page
def homepage(studentName):
    print("GET /schedule/"+studentName)
    from homepage import homepage
    [course_schedule, tutorial_schedule, DDL_schedule] = homepage(studentName)
    weekschedule = {'course':course_schedule, 'tutorial':tutorial_schedule,'DDL':DDL_schedule}
    return render_template('schedule.html', course=weekschedule['course'],tutorial=weekschedule['tutorial'],DDL=weekschedule['DDL'])


@app.route("/schedule/<studentName>/add.html")
def add(studentName):
    print("GET /schedule/<studentName>/add.html")
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    available = "SELECT C.c_code FROM coursebase C WHERE C.c_code NOT IN (SELECT E.c_code FROM enrolled E,student S WHERE S.student_name=%s and S.student_id=E.student_id )"
    cursor.execute(available, [studentName])
    available_course = cursor.fetchall()
    myconn.commit()
    AC=available_course
    return render_template("add.html",choice=AC)

@app.route("/schedule/<studentName>/add")
def addprocess(studentName):
    
    content = request.get_json()
    choice = list(content["choice"])
    print("GET add with choice=", choice, sep="")
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    get_uid_sql = "Select student_id from student Where student_name=%s"
    cursor.execute(get_uid_sql, [studentName])
    uid = cursor.fetchall()[0][0]
    for i in choice:
        sql = "INSERT INTO enrolled VALUES(%s,%s)"
        cursor.execute(sql, [uid,i])
    myconn.commit()
    return json.dumps({"result": "finish"})


@app.route("/schedule/<studentName>/drop.html")
def drop(studentName):
    print("GET /schedule/<studentName>/drop.html")
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    drop = "SELECT E.c_code FROM enrolled E,student S WHERE S.student_name=%s and S.student_id=E.student_id"
    cursor.execute(drop, [studentName])
    drop_course = cursor.fetchall()
    myconn.commit()
    DC=drop_course
    return render_template("drop.html",choice=DC)

@app.route("/schedule/<studentName>/drop")
def dropprocess(studentName):
    content = request.get_json()
    choice = content["choice"]
    print("GET drop with choice=", choice, sep="")
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    get_uid_sql = "Select student_id from student Where student_name=%s"
    cursor.execute(get_uid_sql, [studentName])
    uid = cursor.fetchall()[0][0]
    for i in choice:
        sql = "DELETE FROM enrolled WHERE student_id=%s and c_code=%s"
        cursor.execute(sql, [uid,i])
    myconn.commit()
    return json.dumps({"result": "finish"})

####upcoming page###
@app.route("/upcoming/<studentName>")
###gain data from database and classify them to within 1 hour, with 2 days and other
def upcoming(studentName):
    
    from homepage import homepage
    print("GET /upcoming/"+studentName)
    [course_schedule, tutorial_schedule, DDL_schedule] = homepage(studentName)
    weekschedule = {'course':course_schedule, 'tutorial':tutorial_schedule,'DDL':DDL_schedule}
    weekday=datetime.now().strftime("%a")
    datestr=datetime.now().strftime("%Y-%m-%d")
    currenttimestr = datetime.now().strftime("%H:%M:%S")
    currenttime = datetime.strptime(currenttimestr,"%H:%M:%S")
    date = datetime.strptime(datestr,"%Y-%m-%d")
    within1hour={'course':[],'tutorial':[]}
    within2days={'DDL':[]}
    other={'course':[],'tutorial':[],'DDL':[]}
    for i in weekschedule:
        if i == 'course' or i == 'tutorial':
            for j in weekschedule[i]:
                time=datetime.strptime(j[2],"%H:%M:%S")
                if j[1]==weekday and time>currenttime and time-currenttime<=timedelta(hours=1):
                    within1hour[i].append(j)
                else:
                    other[i].append(j)
        elif i == 'DDL':
            for j in weekschedule[i]:
                ddldate=datetime.strptime(j[1],"%Y-%m-%d")
                print(ddldate-date)
                if ddldate>date and ddldate-date<=timedelta(days=2):
                    within2days[i].append(j)
                else:
                    other[i].append(j)
    
    return json.dumps({"upcomingcourse":within1hour,"upcomingDDL":within2days,'other':other})




if __name__ == "__main__":
    app.run(debug=True)
