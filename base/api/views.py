from http.client import HTTPResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework import views as api_views

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
#from rest_framework_simplejwt.serializers import User as TokenUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .. import models

from .serializers import StudentSerializer, ParaescolarSerializer #, CustomTokenObtainPairSerializer
from .utility.csv_reader import file_to_students
from .utility.csv_reader import remove_accents
from .utility.xlsx import xlsx_grupos, xlsx_paraescolares
from .utility.csv import csv_paraescolares, csv_grupos

from django.http import FileResponse, JsonResponse, HttpResponse
from rest_framework import viewsets, renderers
from rest_framework.decorators import action

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        #token['name'] = user.username
        # ...
        
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#class EmailTokenObtainPairView(TokenObtainPairView):
    #serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteStudent(request):
    data = request.data
    matricula = data['matricula']
    student = models.Student.objects.get(matricula=matricula)

    if student:
        student.delete()
        return JsonResponse({'message' : f'El alumno con matrícula {matricula} fue eliminado'})

    return JsonResponse({'error' : f'No se encontró el alumno con la matrícula {matricula}'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStudents(request):
    #print(request)
    #print(request.GET)
    #print(request.headers)
    students = models.Student.objects.all()
    #print(students.values())
    obj = StudentSerializer(students, many=True)

    return Response(obj.data)


class FileUploadView(api_views.APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def patch(self, request, filename, format=None):
        try:
            file_obj = request.data['file']
            student_list = file_to_students(file_obj)

            obj_list = [models.Student(**student_dict) for student_dict in student_list]
            
            objs = models.Student.objects.bulk_create(obj_list)
            return JsonResponse({'message' : 'Alumnos agregados con éxito!'})
        except Exception as e:
            return JsonResponse({'error' : str(e)})

class GetStudent(api_views.APIView):

    def get(self, request, matricula, format=None):
        try:
            #print(int(matricula[2:4].lstrip('0')))
            student = models.Student.objects.filter(matricula=matricula)
            if student:
                stu = StudentSerializer(student.first())
                return Response(stu.data)
            
            return JsonResponse({'error' : 'No se encontró un alumno con la matrícula proporcionada'})
        except Exception as e:
            return JsonResponse({'error' : str(e)})



@api_view(['GET'])
def wakeView(request):
    return JsonResponse({'message' : 'OK'})

@api_view(['POST'])
def validateView(request):
    try:        
        data = request.data
        #print(data)
        matricula = str(data['matricula'])

        if matricula == "":
            pass
        elif not matricula.isdigit():
            return JsonResponse({'error' : 'La matrícula solo puede contener números'})

        elif len(matricula) != 8:
            return JsonResponse({'error' : 'La matrícula no tiene el tamaño correcto'})

    

        if 'apellido_paterno' in data and data['apellido_paterno']:
            apellido_paterno = data['apellido_paterno'] + ' '
        else:
            return JsonResponse({'error' : 'Se necesita un apellido paterno.',
                                'turno' : student.turno
                                })

        if 'apellido_materno' in data and data['apellido_materno']:
            apellido_materno = data['apellido_materno'] + ' '
        else :
            apellido_materno = ''

        nombres = data['nombres']

        nombre = apellido_paterno + apellido_materno + nombres
        nombre = remove_accents(nombre).upper()

        #print(f'nombre: {nombre}, matrícula: {matricula}')

        try:
            student = models.Student.objects.get(nombre_completo=nombre, matricula=matricula)
        except:
            student = None

        if student:
            if student.tiene_paraescolar:
                return JsonResponse({'error' : f'El alumno ya está inscrito en la paraescolar {student.paraescolar}'})
                
            obj = StudentSerializer(student)
            return Response(obj.data)

        return JsonResponse({'error' : 'No se encontró el alumno con los datos proporcionados.'})
    except Exception as e:
        return JsonResponse({'error' : str(e)})

@api_view(['POST'])
def selectView(request):
    try: 
        data = request.data
        #print(data)
        matricula = data['matricula']
        apellido_paterno = data['apellido_paterno']
        apellido_materno = data['apellido_materno']
        nombres = data['nombres']
        eleccion = data['eleccion']

        if matricula == "":
            pass

        elif not matricula.isdigit():
            return JsonResponse({'error' : 'La matrícula solo puede contener números'})
        elif len(matricula) != 8:
            return JsonResponse({'error' : 'La matrícula no tiene el tamaño correcto'})

        #plantel = int(matricula[2:4].lstrip('0'))
        plantel = 8

        if 'apellido_paterno' in data and data['apellido_paterno']:
            apellido_paterno = data['apellido_paterno'] + ' '
        else:
            return JsonResponse({'error' : 'Se necesita un apellido paterno.',
                                'turno' : student.turno
                                })

        if 'apellido_materno' in data and data['apellido_materno']:
            apellido_materno = data['apellido_materno'] + ' '
        else :
            apellido_materno = ''

        nombres = data['nombres']

        nombre = apellido_paterno + apellido_materno + nombres
        nombre = remove_accents(nombre).upper()

        print(f'nombre: {nombre}, matrícula: {matricula}')

        try:
            student = models.Student.objects.get(nombre_completo=nombre, matricula=matricula)
        except:
            student = None    
        
        if student:
            if student.tiene_paraescolar:
                return JsonResponse({'error' : f'El alumno ya está inscrito en la paraescolar {student.paraescolar}'})
                
            print(student.turno)
            paraescolar = models.Paraescolar.objects.get(nombre=eleccion, turno=student.turno, plantel=plantel)
            print('aaaaaaaa')
            print(paraescolar.alumnos_inscritos)
            if paraescolar:
                if paraescolar.alumnos_inscritos < paraescolar.cupo_total:
                    student.paraescolar = eleccion
                    student.tiene_paraescolar = True

                    paraescolar.alumnos_inscritos = paraescolar.alumnos_inscritos + 1

                    student.save()
                    paraescolar.save()

                    return JsonResponse({'message' : 'La selección fue exitosa!'})
                else: 
                    return JsonResponse({'error' : 'Las paraescolares seleccionadas ya no cuentan con espacio.'})
            else:
                return JsonResponse({'error' : 'No se encontró la paraescolar indicada'})

        return JsonResponse({'error' : 'No se encontró el alumno con los datos proporcionados'})
    except Exception as e:
        print(e)
        return JsonResponse({'error' : e.message})


@permission_classes([IsAuthenticated])
@api_view(['PATCH'])
def changeView(request):
    try: 
        data = request.data
        #print(data)
        matricula = data['matricula']
        eleccion = data['eleccion']
        turno = data['turno']

        if matricula == "":
            pass

        elif not matricula.isdigit():
            return JsonResponse({'error' : 'La matrícula solo puede contener números'})

        elif len(matricula) != 8:
            return JsonResponse({'error' : 'La matrícula no tiene el tamaño correcto'})

        #plantel = int(matricula[2:4].lstrip('0'))
        plantel = 8

        try:
            student = models.Student.objects.get(matricula=matricula, turno=turno)
        except:
            student = None  

        para = models.Paraescolar.objects.filter(nombre=eleccion, turno=turno, plantel=plantel)
        if not para:
            return JsonResponse({'error' : 'No se encontró la paraescolar indicada'})
            
        if student:
            if student.tiene_paraescolar:
                if student.paraescolar == eleccion:
                    return JsonResponse({'error' : f'El alumno seleccionado ya está en la paraescolar de {eleccion}!'})
                previa = models.Paraescolar.objects.get(nombre=student.paraescolar, turno=turno)
                proxima = models.Paraescolar.objects.get(nombre=eleccion, turno=turno)

                if proxima.alumnos_inscritos < proxima.cupo_total:
                    previa.alumnos_inscritos = previa.alumnos_inscritos - 1
                    proxima.alumnos_inscritos = proxima.alumnos_inscritos + 1
                    previa.save()
                    proxima.save()

                else:
                    return JsonResponse({'error' : 'La paraescolar seleccionada ya no tiene cupo'})

            else:
                proxima = models.Paraescolar.objects.get(nombre=eleccion, turno=turno, plantel=plantel)
                
                if proxima and proxima.alumnos_inscritos < proxima.cupo_total:
                    proxima.alumnos_inscritos = proxima.alumnos_inscritos + 1
                    proxima.save()

                else:
                    return JsonResponse({'error' : 'La paraescolar seleccionada ya no tiene cupo'})
                
            
            prev_name = student.paraescolar
            student.paraescolar = eleccion
            student.tiene_paraescolar = True
            student.save()

            if student.tiene_paraescolar:            
                return JsonResponse({'message' : f'La paraescolar del alumno/a con matrícula {matricula} se cambió exitosamente de {prev_name} a {eleccion}'})
            else:
                return JsonResponse({'message' : f'La paraescolar del alumno/a con matrícula {matricula} se cambió exitosamente de ninguna a {eleccion}'})


        return JsonResponse({'error' : 'No se encontró el alumno con los datos proporcionados'})
    except Exception as e:
        print(e)
        return JsonResponse({'error' : e.message})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkTokenView(request):
    return JsonResponse({'message' : 'OK'})


@api_view(['PATCH'])
def removeView(request):
    try:
        data = request.data
        #print(data)
        matricula = data['matricula']

        if matricula == "":
            pass

        elif not matricula.isdigit():
            return JsonResponse({'error' : 'La matrícula solo puede contener dígitos'})

        elif len(matricula) != 8:
            return JsonResponse({'error' : 'La matrícula no tiene el tamaño correcto'})

        #plantel = int(matricula[2:4].lstrip('0'))
        plantel = 8

        if 'apellido_paterno' in data:
            apellido_paterno = data['apellido_paterno'] + ' '
        else:
            apellido_paterno = ''

        if 'apellido_materno' in data:
            apellido_materno = data['apellido_materno'] + ' '
        else :
            apellido_materno = ''

        nombres = data['nombres']
        nombre = apellido_paterno + apellido_materno + nombres
        nombre = remove_accents(nombre).upper()
        

        student = models.Student.objects.get(nombre_completo=nombre, matricula=matricula)

        if student:
            if student.paraescolar:
                paraescolar = models.Paraescolar.objects.get(nombre=student.paraescolar, turno=student.turno, plantel=plantel)
                paraescolar.alumnos_inscritos = paraescolar.alumnos_inscritos - 1
                paraescolar.save()
                
            student.paraescolar = None
            student.tiene_paraescolar=False
            student.save()
            return JsonResponse({'message' : 'El alumno ya no tiene paraescolar.'})   

        return JsonResponse({'error' : 'El alumno no existe!'})
    except Exception as e:
        print(e)
        return JsonResponse({'error' : str(e)})


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def xlsxParaescolarView(request):
    data = request.data
    print(data)
    #paraescolar = data['paraescolar']
    #turno = data['turno']
    paraescolar = 'robotica'
    turno = 'matutino'

    students = models.Student.objects.filter(paraescolar=paraescolar, turno=turno)

    students = students.values()
    filename = xlsx_paraescolares(students, paraescolar, turno)
    filepath = 'base/api/utility/' + filename
    file_handle = open(filepath, 'rb')

    response = FileResponse(file_handle, content_type='whatever')
    print('get real')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #response['Content-Length'] = len(response.content)
    print('got real')

    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def csvParaescolarView(request):
    data = request.data
    print(data)
    paraescolar = data['paraescolar']
    turno = data['turno']
    plantel = 8
    if 'plantel' in data:
        plantel = data['plantel']
    #paraescolar = 'robotica'
    #turno = 'matutino'
    students = models.Student.objects.filter(paraescolar=paraescolar, turno=turno, plantel=plantel)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{paraescolar}-{turno}-{plantel}.csv"'


    students = list(students.values())
    csv_paraescolares(students, response)

    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def csvGroupView(request):
    data = request.data
    print(data)
    grupo = data['grupo']
    plantel = 8
    if 'plantel' in data:
        plantel = data['plantel']
    #grupo = '609'

    students = models.Student.objects.filter(grupo=grupo, plantel=plantel)
    students = students.values()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{grupo}-{plantel}.csv"'

    csv_grupos(students, response)
    

    return response    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changeStudentTurn(request):
    matricula = request.data['matricula']
    nombre_completo = request.data['nombre_completo']
    student = models.Student.objects.get(matricula=matricula, nombre_completo=nombre_completo)

    if student.turno == "MATUTINO":
        student.turno = "VESPERTINO"
        student.grupo = str(50 + int(student.grupo))
    else:
        student.turno = "MATUTINO"
        student.grupo = str(int(student.grupo) - 50)
    
    student.save()
    return Response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def xlsxGroupView(request):
    data = request.data
    print(data)
    grupo = data['grupo']
    #grupo = '609'

    students = models.Student.objects.filter(grupo=grupo)
    students = students.values()
    filename = xlsx_grupos(students, grupo)
    filepath = 'base/api/utility/' + filename
    file_handle = open(filepath, 'rb')

    response = FileResponse(file_handle, content_type='whatever')
    print('get real')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    #response['Content-Length'] = len(response.content)
    print('got real')

    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def makeParaescolarView(request):
    try:
        data = request.data
        paraescolar = data['nombre']
        cupo = data['cupo_total']
        turno = None
        #if 'turno' in data and data['turno']:
        turno = data['turno']
        plantel = 8
        if 'plantel' in data:
            plantel = int(data['plantel'])
        
        if turno == 'AMBOS':
            matPara = models.Paraescolar(nombre=paraescolar, cupo_total=cupo, alumnos_inscritos=0, turno="MATUTINO", plantel=plantel)
            vesPara = models.Paraescolar(nombre=paraescolar, cupo_total=cupo, alumnos_inscritos=0, turno="VESPERTINO", plantel=plantel)
            matPara.save()
            vesPara.save()

        else:
            newPara = models.Paraescolar(nombre=paraescolar, cupo_total=cupo, alumnos_inscritos=0, turno=turno, plantel=plantel)
            newPara.save()
            
        return JsonResponse({'message' : 'La paraescolar se creó con éxito!'})
    except Exception as e:
        return JsonResponse({'error' : str(e)})


@api_view(['POST'])
def getParaescolarView(request):
    print('Begin request')
    data = request.data
    paraescolar = data['nombre']
    turno = data['turno']

    plantel = 8
    if 'plantel' in data:
        plantel = int(data['plantel'])
    
    print(f'Get {paraescolar}-{turno}')
    para = models.Paraescolar.objects.get(nombre=paraescolar, turno=turno, plantel=plantel)
    obj = ParaescolarSerializer(para)

    return Response(obj.data)


@api_view(['GET'])
def getAllParaescolarView(request):

    para = models.Paraescolar.objects.all()
    obj = ParaescolarSerializer(para, many=True)

    return Response(obj.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def changeParaescolarView(request):
    try:
        data = request.data
        paraescolar = data['nombre']
        turno = data['turno']
        plantel = 8

        if 'plantel' in data:
            plantel = int(data['plantel'])

        para = models.Paraescolar.objects.filter(nombre=paraescolar, turno=turno, plantel=plantel)

        if 'nuevo_cupo' in data and data['nuevo_cupo']:
            nuevo_cupo = data['nuevo_cupo']
            if nuevo_cupo < para.alumnos_inscritos:
                return JsonResponse({'error' : f'No se puede reducir el cupo porque la paraescolar tiene {para.alumnos_inscritos} alumnos inscritos.'})
            para.update(nombre=nuevo_cupo)

        if 'nuevo_nombre' in data and data['nuevo_nombre']:
            nuevo_nombre = data['nuevo_nombre']
            para.update(nombre=nuevo_nombre)

            students = models.Student.objects.filter(paraescolar=paraescolar, turno=turno)
            students.update(paraescolar=nuevo_nombre)


        #if 'nuevo_nombre' in data and data['nuevo_nombre']:
            #nuevo_nombre = data['nuevo_nombre']
            #para.update(nombre=nuevo_nombre)

            
        #nuevo_cupo = data['nuevo_cupo']
        
        return JsonResponse({'message' : f'La paraescolar se actualizó exitosamente!'})

        
            
    except Exception as e:
        return JsonResponse({'error' : str(e)}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteParaescolarView(request):
    try:
        data = request.data
        paraescolar = data['nombre']
        turno = data['turno']
        plantel = 8
        if 'plantel' in data:
            plantel = int(data['plantel'])

        para = models.Paraescolar.objects.filter(nombre=paraescolar, turno=turno, plantel=plantel)

        if para:
            para.delete()
            students = models.Student.objects.filter(paraescolar=paraescolar, turno=turno)
            if students.exists():
                students.update(paraescolar=None, tiene_paraescolar=False)            
                
            return JsonResponse({'message' : 'La paraescolar fue eliminada exitosamente!'})
        return JsonResponse({'error' : 'No se encontró la paraescolar con los datos proporcionados.'})
        

    except Exception as e:
        return JsonResponse({'error' : str(e)}, status=500)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getGroupList(request):
    try:
        data = request.data
        grupo = data['grupo']
        students = models.Student.objects.filter(grupo=grupo)
        obj = StudentSerializer(students, many=True).data

        res = sorted(obj, key = lambda x : x['nombre_completo'])

        return Response(res)
    except Exception as e:
        return JsonResponse({'error' : str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getParaescolarList(request):
    data = request.data
    paraescolar = data['nombre']
    turno = data['turno']

    students = models.Student.objects.filter(paraescolar=paraescolar, turno=turno)
    obj = StudentSerializer(students, many=True).data

    res = sorted(obj, key = lambda x : x['nombre_completo'])

    return Response(res)


@api_view(['POST'])
def teacherRegister(request):
    data = request.data
    email = data['email']
    username = data['username']
    password = data['password']

    
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'error' : 'El correo proporcionado tiene un formato incorrecto.'})
    else:
        email_parts = email.split('@')

        if email_parts[1] != 'cobachih.edu.mx':
            return JsonResponse({'error' : 'El correo proporcionado debe ser insitucional (@cobachih.edu.mx)'})

        if email_parts[0].isdigit():
            return JsonResponse({'error' : 'El correo proporcionado debe ser de un docente'})
        
        User.objects.create_user(username, email, password)

        return JsonResponse({'message' : 'Creación exitosa, pero aún no se implementa la verificación por correo'})

@api_view(['GET'])
def getGroups(request):
    groups = list(models.Student.objects.order_by().values_list('grupo').distinct())
    groups = sorted([x[0] for x in groups])
    return Response(groups)