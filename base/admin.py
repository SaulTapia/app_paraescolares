from django.contrib import admin
from .models import Student, Paraescolar
# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'grupo', 'matricula', 'plantel', 'paraescolar')


@admin.register(Paraescolar)
class ParaescolarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'turno', 'plantel', 'alumnos_inscritos', 'cupo_total')

