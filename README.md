# COMP3278 API

[main.py](./main.py) contains all flask functions needed [Take a Look](./main.py)

**########### IMPORTANT: changes to public SQL file ###########**
* Change time_zone to "+08:00" 
  * originally "+00:00"
* Change Table "Student": replace "name.first" and "name.last" with "student_name"
  * Seems that MySQL does not support composite attributes [link](https://stackoverflow.com/questions/23396988/create-a-composite-attribute-in-my-sql-er-diagram)

## Login

`GET` | Response | description | example
--- | --- | --- | ---
`/` | text/html | load index.html | N/A
`/faceLogin.html` | text/html | load faceLogin.html | N/A
`/faceRegister.html` | text/html | load faceRegister.html | N/A
`/faceLogin` | application/json | start face recognition; return studentName if face recoginized, else "None" | {"value": "None"} or {"value": "Loridy"}
`/homepage/<studentName>/logout` | application/json | logout (used to store logout time) | {"result": "Log out successfully"}

### Welcome message when user login (student name, login time) <br> Done with JS?

## Register

`POST` | Request | example| Response | description | example
--- | --- | --- | --- | --- | ---
`/faceRegister` | application/json | {"studentName": str, "studentId": str, "email": str, "department": str, "moodle": str} | text | register a new account; after fill in all info, start face capture | "OK"
