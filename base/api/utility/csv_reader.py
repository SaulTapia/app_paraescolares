import pandas as pd
import unicodedata
import re

def remove_accents(input_str):
    #print(f'Called with input {input_str}')
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def make_turn(group):
    #print(f'Group {group}')
    group = int(group) % 100
    if group < 25: return "MATUTINO"
    else: return "VESPERTINO"

def strip(stri):
    return stri.strip(' ')

def get_plantel(matricula):
    #print(f'Matricula {matricula}')

    if matricula == "":
        return 8
    mat = matricula[2:4].lstrip('0')
    return int(mat)

def make_name(nombre_completo):
    return re.sub(' +', ' ', nombre_completo)

def remove_dot(mat):
    #print(f'returning {mat.split(".")[0]}')
    return mat.split('.')[0]

def file_to_students(file):
    df = pd.read_csv(file, index_col=False)

    df.columns = ['apellido_paterno', 'apellido_materno', 'nombres', 'grupo', 'matricula']
    df.fillna("", inplace=True)
    #print("AAAAAAAAa")
    df['matricula'] = df['matricula'].astype('str')
    df['matricula'] = df['matricula'].apply(remove_dot)

    #print("CCCCCCCCCCCC")
    
    df['grupo'] = df['grupo'].astype('str')
    #print(df.head())

    #print(df)

    df['apellido_paterno'] = df['apellido_paterno'].apply(strip)
    df['apellido_materno'] = df['apellido_materno'].apply(strip)
    df['nombres'] = df['nombres'].apply(strip)
    df['grupo'] = df['grupo'].apply(strip)
    df['matricula'] = df['matricula'].apply(strip)
    df['turno'] = df['grupo'].apply(make_turn)

    

    for column in ['nombres', 'apellido_paterno', 'apellido_materno']:
        df[column] = df[column].apply(remove_accents).str.upper()

    df['nombre_completo'] = df['apellido_paterno'] + ' ' + df['apellido_materno'] + ' ' + df['nombres']
    df['nombre_completo'] = df['nombre_completo'].apply(make_name)
    df = df.drop(['apellido_materno', 'apellido_paterno', 'nombres'], axis = 1)
    #name_data = df['nombre_completo'].apply(separate_name)
    #df = pd.concat([df.drop(['nombre_completo'], axis=1), name_data.apply(pd.Series)], axis=1)
    
    df['plantel'] = df['matricula'].apply(get_plantel)

    #print(df.head())
    dict = df.to_dict('records')
    return dict
