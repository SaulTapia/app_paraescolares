# app_paraescolares
API en django para app manejo de paraescolares

# Endpoints

| Endpoint                           | Método  | Recibe                   | Regresa                      |
| ---------------------------------- |:-------:|:------------------------:|:----------------------------:|
| /api/token                         | POST    |username, password        |Refresh & access tokens       |
| /api/token/refresh                 | POST    |Refresh token             |Refresh & access tokens       |
| /api/students                      | GET     |Access token              |Array de todos los estudiantes|
| /api/students/upload/<archivo.csv> | PUT     |Access token & archivo.csv|200 OK / 401 Unauthorized     |
| /api/wake/                         | GET     |                          |200 OK                        |
| /api/select/                       | POST    |nombres, apellido_paterno, apellido_materno, matricula, elección|200 OK / 404 not found|
| /api/select/validate/              | GET     |nombres, apellido_paterno, apellido_materno, matricula|200 OK / 404 not found|
| /api/select/remove/ <br />(DEBUG, QUITAR ANTES DE PRODUCCIÓN)  | PUT    |nombres, apellido_paterno, apellido_materno, matricula|200 OK / 404 not found|
| /api/xlsx/group/                   | GET     |grupo                     |Xlsx con alumnos del grupo    |
| /api/xlsx/paraescolar/             | GET     |nombre, turno             |Xlsx con alumnos de la paraescolar|
| /api/list/group/                   | GET     |grupo                     |Array con alumnos del grupo   |
| /api/list/paraescolar/             | GET     |nombre, turno             |Array con alumnos de la paraescolar|
| /api/paraescolares/getall/         | GET     |                          |Array con datos de todas las paraescolares|
| /api/paraescolares/make/           | POST    |nombre, turno, cupo_total |200 OK                        |
| /api/paraescolares/delete/         | DELETE  |nombre, turno             |200 OK                        |

# Formato de archivos .csv
```apellido_paterno,apellido_materno,nombres,grupo,matricula```
### Ejemplo de archivo .csv:
```
apellido_paterno,apellido_materno,nombres,grupo,matricula
Tapia,Loya,Saúl Alejandro,609,19080045
Pancho,Poncho,Trijo Trajo,452,19053482
Pérez,Sánchez,Juan Pablo,356,19392308
```
