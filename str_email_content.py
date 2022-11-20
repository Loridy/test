from homepage import homepage
from datetime import datetime, timedelta

# return str type info of within1hour course/tutorial
def str_email_content(studentName):
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
                if ddldate>date and ddldate-date<=timedelta(days=2):
                    within2days[i].append(j)
                else:
                    other[i].append(j)
    x=''
    for i in within1hour:
        for j in within1hour[i]:
            x=x+','.join(j)+'\n'
    return x