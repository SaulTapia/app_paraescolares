from rest_framework import serializers
#from api.models import  User
from ..models import Student, Paraescolar

#class UserSerializer(serializers.ModelSerializer):
  #class Meta:
      #model = User
      #fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
  class Meta:
      model = Student
      fields = "__all__"

class ParaescolarSerializer(serializers.ModelSerializer):
  class Meta:
      model = Paraescolar
      fields = "__all__"      