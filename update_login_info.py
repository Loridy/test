import mysql.connector
from datetime import datetime
def update_login_info(student_name):
    # login info
    time = datetime.now()
    print(time)
    # time = now.strftime("%H:%M:%S")
    student_name = student_name.replace("_", " ")
    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    get_uid_sql = "SELECT student_id from student WHERE student_name=%s"
    cursor.execute(get_uid_sql, [student_name]) # always true
    uid = cursor.fetchall()[0][0]

    get_behavior_id = "SELECT behaviour_id from login_record Where student_id=%s"
    cursor.execute(get_behavior_id, [uid])
    behaviour_id = cursor.fetchall()
    if behaviour_id == []:
        behaviour_id = 1
    else:
        behaviour_id = behaviour_id[-1][0]
        behaviour_id += 1
    # problem: hard to trace logout time
    sql = "INSERT INTO `login_record` (`student_id`, `behaviour_id`, `login_time`) VALUE (%s, %s, %s)"
    cursor.execute(sql, [uid, behaviour_id, time])
    print(time)
    myconn.commit()

