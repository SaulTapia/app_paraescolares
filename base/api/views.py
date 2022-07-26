from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework import views as api_views

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .. import models

from .serializers import StudentSerializer
from .utility.csv_reader import file_to_students
from .utility.csv_reader import remove_accents


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
    print(request)
    print(request.GET)
    print(request.headers)
    students = models.Student.objects.all()
    obj = StudentSerializer(students, many=True)

    return Response(obj.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadStudents(request):
    
    students = models.Student.objects.all()
    obj = StudentSerializer(students, many=True)

    return Response(obj.data)

paraescolares = [
    'robotica',
]
# views.py
class FileUploadView(api_views.APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        student_list = file_to_students(file_obj)
        obj_list = [models.Student(**student_dict) for student_dict in student_list]
        objs = models.Student.objects.bulk_create(obj_list)
        return Response(status=204)

@api_view(['GET'])
def wakeView(request):
    return Response()

@api_view(['GET'])
def validateView(request):
    try:        
        data = request.data
        #print(data)
        matricula = data['matricula']
        apellido_paterno = data['apellido_paterno']
        apellido_materno = data['apellido_materno']
        nombres = data['nombres']

        nombre = apellido_paterno + ' ' + apellido_materno + ' ' + nombres
        nombre = remove_accents(nombre).upper()
        #print(f'nombre: {nombre}, matrícula: {matricula}')

        student = models.Student.objects.filter(nombre_completo=nombre, matricula=matricula)
        if student:
            return Response()

        return Response(status=404)
    except:
        return Response(status=400)

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

        nombre = apellido_paterno + ' ' + apellido_materno + ' ' + nombres
        nombre = remove_accents(nombre).upper()
        #print(f'nombre: {nombre}, matrícula: {matricula}')

        student = models.Student.objects.filter(nombre_completo=nombre, matricula=matricula, tiene_paraescolar=False)

        if student:
            if eleccion in paraescolares:
                student.update(paraescolar=eleccion, tiene_paraescolar=True)
                return Response()

            return Response(status=400)

        return Response(status=404)
    except:
        return Response(status=400)

@api_view(['PUT'])
def removeView(request):
    try:
        data = request.data
        #print(data)
        matricula = data['matricula']
        apellido_paterno = data['apellido_paterno']
        apellido_materno = data['apellido_materno']
        nombres = data['nombres']

        nombre = apellido_paterno + ' ' + apellido_materno + ' ' + nombres
        nombre = remove_accents(nombre).upper()
        #print(f'nombre: {nombre}, matrícula: {matricula}')

        student = models.Student.objects.filter(nombre_completo=nombre, matricula=matricula)

        if student:
            student.update(paraescolar=None, tiene_paraescolar=False)
            return Response()   

        return Response(status=404)
    except:
        return Response(status=400)