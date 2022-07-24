# app_paraescolares
API en django para app manejo de paraescolares

# Endpoints

| Endpoint                           | Método  | Recibe                   | Regresa                      |
| ---------------------------------- |:-------:|:------------------------:|:----------------------------:|
| /api/token                         | POST    |Username, password        |Refresh & access tokens       |
| /api/token/refresh                 | POST    |Refresh token             |Refresh & access tokens       |
| /api/students                      | GET     |Access token              |Array de todos los estudiantes|
| /api/students/upload/<archivo.csv> | PUT     |Access token & archivo.csv|200 OK / 101 Permission Denied|

# Formato de archivos .csv
```apellido_paterno,apellido_materno,nombres,grupo,matricula```
### Ejemplo de archivo .csv:
```
apellido_paterno,apellido_materno,nombres,grupo,matricula
Tapia,Loya,Saúl Alejandro,609,19080045
Pancho,Poncho,Trijo Trajo,452,19053482
Pérez,Sánchez,Juan Pablo,356,19392308
```
