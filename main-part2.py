from flask import Flask, render_template, request
from flask_restful import Api, Resource
import mysql.connector
from datetime import datetime, timedelta
import json

app = Flask(__name__, template_folder="./html")
api = Api(app)


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
    print("GET add with choice="+choice)
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
    print("GET drop with choice="+choice)
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
