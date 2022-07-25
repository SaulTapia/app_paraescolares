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

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
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
    students = models.Student.objects.all()
    obj = StudentSerializer(students, many=True)

    return Response(obj.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadStudents(request):
    
    students = models.Student.objects.all()
    obj = StudentSerializer(students, many=True)

    return Response(obj.data)


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