from rest_framework import serializers
#from api.models import  User
from ..models import Student, Paraescolar
from rest_framework_simplejwt.tokens import RefreshToken
#from rest_framework_simplejwt.serializers import User
from django.contrib.auth.models import User

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
    

#from rest_framework_simplejwt.serializers import TokenObtainSerializer

# class EmailTokenObtainSerializer(TokenObtainSerializer):
#     username_field = User.EMAIL_FIELD


# class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
#     @classmethod
#     def get_token(cls, user):
#         return RefreshToken.for_user(user)

#     def validate(self, attrs):
#         data = super().validate(attrs)

#         refresh = self.get_token(self.user)

#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)

#         return data