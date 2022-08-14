# app_paraescolares
API en django para app manejo de paraescolares

# Endpoints

| Endpoint                           | Método  | Recibe                   | Regresa                      | Require autenticación |
| ---------------------------------- |:-------:|:------------------------:|:----------------------------:|:---------------------:|
| /api/token                         | POST    |username, password        |Refresh & access tokens       |No
| /api/token/refresh                 | POST    |Refresh token             |Refresh & access tokens       |No
| /api/students                      | GET     |Access token              |Array de todos los estudiantes|Sí
| /api/students/\<matricula>/         | GET     |Access token              |Objeto con datos del alumno   |Sí
| /api/students/upload/<archivo.csv> | PATCH   |Access token & archivo.csv|200 OK / 401 Unauthorized     |Sí
| /api/wake/                         | GET     |                          |200 OK                        |No
| /api/select/                       | POST    |nombres, apellido_paterno, apellido_materno, matricula, eleccion|200 OK / 404 not found|No|
| /api/select/validate/              | POST    |nombres, apellido_paterno, apellido_materno, matricula|200 OK / 404 not found|No|
| /api/select/remove/ <br />(DEBUG, QUITAR ANTES DE PRODUCCIÓN)  | PATCH    |nombres, apellido_paterno, apellido_materno, matricula|200 OK / 404 not found|No|
| /api/select/change/                | PATCH   |matricula, eleccion, turno|200 OK                        |Sí|
| /api/xlsx/group/                   | POST    |grupo                     |Xlsx con alumnos del grupo    |Sí|
| /api/xlsx/paraescolar/             | POST    |nombre_paraescolar, turno             |Xlsx con alumnos de la paraescolar|Sí|
| /api/list/group/                   | POST    |grupo                     |Array con alumnos del grupo   |Sí|
| /api/list/paraescolar/             | POST    |nombre_paraescolar, turno             |Array con alumnos de la paraescolar|Sí|
| /api/paraescolares/getall/         | GET     |                          |Array con datos de todas las paraescolares|No|
| /api/paraescolares/make/           | POST    |nombre, turno, cupo_total |200 OK                        |Sí|
| /api/paraescolares/delete/         | DELETE  |nombre, turno             |200 OK                        |Sí|
| /api/teacher/register/             | POST    |userame, password, email  |200 OK                        |No|

# Formato de archivos .csv
```apellido_paterno,apellido_materno,nombres,grupo,matricula```
### Ejemplo de archivo .csv:
```
apellido_paterno,apellido_materno,nombres,grupo,matricula
Tapia,Loya,Saúl Alejandro,609,19080045
Pancho,Poncho,Trijo Trajo,452,19053482
Pérez,Sánchez,Juan Pablo,356,19392308
```
