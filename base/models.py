from django.db import models

# Create your models here.
class Student(models.Model):    
    nombre_completo = models.CharField(max_length=200, null=True)
    grupo = models.CharField(max_length=50)
    paraescolar = models.CharField(max_length=200, null=True)
    matricula = models.CharField(max_length=30)
    turno = models.CharField(max_length=50)
    turno = models.CharField(max_length=50)
    tiene_paraescolar = models.BooleanField(default=False)
    


    def __str__(self):
        return self.nombre_completo
