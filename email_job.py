import mysql.connector
# Below are packages for sending an 'upcoming' email
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

def email_job(studentName):

    ############### Get the email address of this student from DB #################

    myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
    cursor = myconn.cursor()
    get_emailaddr_sql = "Select email from student Where student_name=%s"
    cursor.execute(get_emailaddr_sql, [studentName])
    emailaddr = cursor.fetchall()[0]
    myconn.commit()

    ############### Connect to the sender #################

    host_server = "smtp.126.com"  # smtp server address
    sender_sina = 'max_19841984@126.com'  # email address of sender
    pwd = 'AQEAHSGQVLBRSVZX'  # PIN
    sender_sina_mail = 'max_19841984@126.com'  # email address of sender
    receiver = emailaddr  # email address of receiver

    ############### edit the content of an email #################
    from str_email_content import str_email_content

    mail_title = 'Upcoming_in_one_hour'
    mail_content = str_email_content(studentName)  # get str(within1hour) from DB
    msg = MIMEMultipart()
    msg['Subject'] = Header(mail_title, 'utf-8')
    msg['From'] = sender_sina_mail
    msg['To'] = Header(receiver, 'utf-8')
    msg.attach(MIMEText(mail_content, 'html', 'utf-8'))

    ############### to send the email #################
    try:
        smtp = SMTP_SSL(host_server)
        smtp.set_debuglevel(0)
        smtp.ehlo(host_server)
        smtp.login(sender_sina, pwd)
        smtp.sendmail(sender_sina_mail, receiver, msg.as_string())
        smtp.quit()
        print('email send success')
    except smtplib.SMTPException:
        print('email send error')

