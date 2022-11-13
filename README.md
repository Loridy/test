# COMP3278 API

## Login


`GET` | Response | description | example
--- | --- | --- | ---
`/` | text/html | load index.html | N/A
`/faceLogin.html` | text/html | load faceLogin.html | N/A
`/faceRegister.html` | text/html | load faceRegister.html | N/A
`/faceLogin` | application/json | start face recognition; return studentName if face recoginized, else "None" | {"value": "None"} or {"value": "Loridy"}
`/homepage/\<studentName\>/logout` | application/json | logout (used to store logout time) | {"result": "Log out successfully"}

## Register

`POST` | Request | example| Response | description | example
--- | --- | --- | --- | --- | ---
`/faceRegister` | application/json | {"studentName": str, "studentId": str, "email": str, "department": str, "moodle": str} | text | register a new account; after fill in all info, start face capture | "OK"
