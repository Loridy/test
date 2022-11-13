import requests
import mysql.connector
import json

BASE = "http://127.0.0.1:5000/"


# # @app.route("/")
# response = requests.get(BASE)
# print(response.text)


# # @app.route("/faceLogin.html")
# response = requests.get(BASE+"faceLogin.html")
# print(response.text)

# # @app.route("/faceRegister.html")
# response = requests.get(BASE+"faceRegister.html")
# print(response.text)
# headers = {"accept": "application/json", "Content-Type": "application/json"}
# data = {
#     "studentName": "Luo Ruidi",
#     "studentId": "3035835648",
#     "email": "luo26@connect.hku.hk",
#     "department": "CS"
# }

# @app.route("/faceLogin", methods=['POST', 'GET'])
# response = requests.get(BASE+"faceRegister", data=json.dumps(data), headers=headers)
# print(response.text)

myconn = mysql.connector.connect(host="localhost", user="root", password="        ", database="COMP3278")
cursor = myconn.cursor()
sql = "Select login_time from login_record Where behaviour_id=1"
cursor.execute(sql)
result = cursor.fetchall()
myconn.commit()
print(result)
# response = requests.get(BASE+"/faceLogin")

# response = requests.put(BASE+"")