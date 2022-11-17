import mysql.connector
from datetime import datetime, timedelta

def homepage(studentName):
    #get course time table
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    course = "SELECT C.c_code,C.c_day, C.c_time_start, C.c_time_end FROM courset C,enrolled E,student S WHERE S.student_name=%s and S.student_id=E.student_id and E.c_code=C.c_code"
    cursor.execute(course, [studentName])
    course_table = cursor.fetchall()
    myconn.commit()
    course_schedule = course_table
    for i in range(len(course_schedule)):
        course_schedule[i]=list(course_schedule[i])
        start = course_schedule[i][2]
        end = course_schedule[i][3]
        zero=datetime(2022,1,1,0,0,0,0)
        newstart=start+zero
        newend=end+zero
        course_schedule[i][2]= newstart.strftime("%H:%M:%S")
        course_schedule[i][3]= newend.strftime("%H:%M:%S")

    



    #get tutorial time table
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    tutorial = "SELECT T.c_code,T.t_day, T.t_time_start, T.t_time_end FROM tutorialbase T,enrolled E,student S WHERE S.student_name=%s and S.student_id=E.student_id and E.c_code=T.c_code"
    cursor.execute(tutorial, [studentName])
    tutorial_table = cursor.fetchall()
    myconn.commit()
    tutorial_schedule = tutorial_table
    for i in range(len(tutorial_schedule)):
        tutorial_schedule[i]=list(tutorial_schedule[i])
        start = tutorial_schedule[i][2]
        end = tutorial_schedule[i][3]
        zero=datetime(2022,1,1,0,0,0,0)
        newstart=start+zero
        newend=end+zero
        tutorial_schedule[i][2]= newstart.strftime("%H:%M:%S")
        tutorial_schedule[i][3]= newend.strftime("%H:%M:%S")

    #get DDL time table
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    DDL = "SELECT D.c_code,D.ddl_date, D.ddl_time FROM DDL D,enrolled E,student S WHERE S.student_name=%s and S.student_id=E.student_id and E.c_code=D.c_code"
    cursor.execute(DDL, [studentName])
    DDL_table = cursor.fetchall()
    myconn.commit()
    DDL_schedule = DDL_table
    for i in range(len(DDL_schedule)):
        DDL_schedule[i]=list(DDL_schedule[i])
        date = DDL_schedule[i][1]
        end = DDL_schedule[i][2]
        zero=datetime(2022,1,1,0,0,0,0)
        newend=end+zero
        DDL_schedule[i][1]= date.strftime("%Y-%m-%d")
        DDL_schedule[i][2]= newend.strftime("%H:%M:%S")

    return course_schedule, tutorial_schedule, DDL_schedule
