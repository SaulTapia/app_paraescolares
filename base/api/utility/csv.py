import csv

def csv_paraescolares(students, response):
    writer = csv.DictWriter(response, fieldnames=['nombre_completo', 'matricula', 'grupo'])
    writer.writeheader()
    for student in students:
        student = {k : v for k, v in student.items() if k in ['nombre_completo', 'matricula', 'grupo']}
        print(student)
        writer.writerow(student)

    
def csv_grupos(students, response):
    writer = csv.DictWriter(response, fieldnames=['nombre_completo', 'matricula', 'paraescolar'])
    writer.writeheader()
    for student in students:
        student = {k : v for k, v in student.items() if k in ['nombre_completo', 'matricula', 'paraescolar']}
        print(student)
        writer.writerow(student)
        