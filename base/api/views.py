from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework import views as api_views

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .. import models

from .serializers import StudentSerializer, ParaescolarSerializer
from .utility.csv_reader import file_to_students
from .utility.csv_reader import remove_accents
from .utility.xlsx import xlsx_grupos, xlsx_paraescolares

from django.http import FileResponse, JsonResponse
from rest_framework import viewsets, renderers
from rest_framework.decorators import action

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


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadStudents(request):
    
    students = models.Student.objects.all()
    obj = StudentSerializer(students, many=True)

    return Response(obj.data)


class FileUploadView(api_views.APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def patch(self, request, filename, format=None):
        file_obj = request.data['file']
        student_list = file_to_students(file_obj)
        obj_list = [models.Student(**student_dict) for student_dict in student_list]
        objs = models.Student.objects.bulk_create(obj_list)
        return Response(status=200)

@api_view(['GET'])
def wakeView(request):
    return JsonResponse({'message' : 'OK'})

@api_view(['POST'])
def validateView(request):
    try:        
        data = request.data
        #print(data)
        matricula = data['matricula']

        if not matricula.isdigit():
            return JsonResponse({'message' : 'Not Found'}, status=404)

        apellido_paterno = data['apellido_paterno']
        apellido_materno = data['apellido_materno']
        nombres = data['nombres']

        nombre = apellido_paterno + ' ' + apellido_materno + ' ' + nombres
        nombre = remove_accents(nombre).upper()
        #print(f'nombre: {nombre}, matrícula: {matricula}')

        student = models.Student.objects.filter(nombre_completo=nombre, matricula=matricula)
        if student:
            return JsonResponse({'message' : 'OK'})

        return JsonResponse({'message' : 'Not Found'}, status=404)
    except:
        return JsonResponse({'message' : 'Not found'}, status=404)

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

        if not matricula.isdigit():
            return JsonResponse({'message' : 'Not Found'}, status=404)

        nombre = apellido_paterno + ' ' + apellido_materno + ' ' + nombres
        nombre = remove_accents(nombre).upper()
        print(f'nombre: {nombre}, matrícula: {matricula}')

        student = models.Student.objects.get(nombre_completo=nombre, matricula=matricula, tiene_paraescolar=False)
                
        
        if student:
            print(student.turno)
            paraescolar = models.Paraescolar.objects.get(nombre=eleccion, turno=student.turno)
            print('aaaaaaaa')
            print(paraescolar.alumnos_inscritos)
            if paraescolar and paraescolar.alumnos_inscritos < paraescolar.cupo_total:
                student.paraescolar = eleccion
                student.tiene_paraescolar = True

                paraescolar.alumnos_inscritos = paraescolar.alumnos_inscritos + 1

                student.save()
                paraescolar.save()

                return JsonResponse({'message' : 'OK'})

            return JsonResponse({'message' : 'Not found'}, status=404)

        return JsonResponse({'message' : 'Not Found'}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'message' : 'Not found'}, status=404)

@api_view(['PATCH'])
def removeView(request):
    try:
        data = request.data
        #print(data)
        matricula = data['matricula']

        if not matricula.isdigit():
            return JsonResponse({'message' : 'Not Found'}, status=404)

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
                paraescolar = models.Paraescolar.objects.get(nombre=student.paraescolar, turno=student.turno)
                paraescolar.alumnos_inscritos = paraescolar.alumnos_inscritos - 1
                paraescolar.save()
                
            student.paraescolar = None
            student.tiene_paraescolar=False
            student.save()
            return JsonResponse({'message' : 'OK'})   

        return JsonResponse({'message' : 'Not Found'}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'message' : 'Not found'}, status=404)


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
    #response['Content-Length'] = len(response.content)
    print('got real')

    return response


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
    data = request.data
    paraescolar = data['nombre']
    cupo = data['cupo_total']
    turno = data['turno']
    
    newPara = models.Paraescolar(nombre=paraescolar, cupo_total=cupo, alumnos_inscritos=0, turno=turno)
    newPara.save()

    return JsonResponse({'message' : 'OK'})


@api_view(['POST'])
def getParaescolarView(request):
    print('Begin request')
    data = request.data
    paraescolar = data['nombre']
    turno = data['turno']
    
    print(f'Get {paraescolar}-{turno}')
    para = models.Paraescolar.objects.get(nombre=paraescolar, turno=turno)
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
    data = request.data
    paraescolar = data['nombre']
    nuevo_nombre = data['nuevo_nombre']
    turno = data['turno']
    
    models.Paraescolar.objects.filter(nombre=paraescolar, turno=turno).update(nombre=nuevo_nombre)

    students = models.Student.objects.filter(paraescolar=paraescolar, turno=turno)
    students.update(paraescolar=nuevo_nombre)
    
        
    return JsonResponse({'message' : 'OK'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteParaescolarView(request):
    data = request.data
    paraescolar = data['nombre']
    turno = data['turno']
    models.Paraescolar.objects.filter(nombre=paraescolar, turno=turno).delete()

    students = models.Student.objects.filter(paraescolar=paraescolar, turno=turno)
    students.update(paraescolar=None, tiene_paraescolar=False)

    
    return JsonResponse({'message' : 'OK'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getGroupList(request):
    data = request.data
    grupo = data['grupo']
    students = models.Student.objects.filter(grupo=grupo)
    obj = StudentSerializer(students, many=True).data

    res = sorted(obj, key = lambda x : x['nombre_completo'])

    return Response(res)

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