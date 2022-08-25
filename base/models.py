from django.db import models

# Create your models here.
class Student(models.Model):    
    nombre_completo = models.CharField(max_length=200, null=False)
    grupo = models.CharField(max_length=50)
    paraescolar = models.CharField(max_length=200, blank=True, null=True)
    matricula = models.CharField(max_length=30, blank=True, null=True)
    turno = models.CharField(max_length=50)
    tiene_paraescolar = models.BooleanField(default=False)
    plantel = models.IntegerField(default=8)


    def __str__(self):
        return self.nombre_completo

    class Meta:
        unique_together = ('nombre', 'grupo', 'plantel', 'matricula')

class Paraescolar(models.Model):    
    nombre = models.CharField(max_length=200, null=False)
    turno = models.CharField(max_length=30, null=False)
    cupo_total = models.IntegerField(null=False)
    alumnos_inscritos = models.IntegerField(null=False)
    plantel = models.IntegerField(default=8)


    def __str__(self):
        return self.nombre

    class Meta:
        unique_together = ('nombre', 'turno', 'plantel')