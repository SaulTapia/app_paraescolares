import pandas as pd
import unicodedata

def remove_accents(input_str):
    print(f'Called with input {input_str}')
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def make_turn(group):
    group = group % 100
    if group < 25: return "MATUTINO"
    else: return "VESPERTINO"


def get_plantel(matricula):
    mat = matricula[2:4].lstrip('0')
    return int(mat)

def file_to_students(file):
    df = pd.read_csv(file, index_col=False)

    #print(df.head())
    df.columns = ['apellido_paterno', 'apellido_materno', 'nombres', 'grupo', 'matricula']
    df['turno'] = df['grupo'].apply(make_turn)
    df['matricula'] = df['matricula'].astype('str')

    for column in ['nombres', 'apellido_paterno', 'apellido_materno']:
        df[column] = df[column].apply(remove_accents).str.upper()

    df['nombre_completo'] = df['apellido_paterno'] + ' ' + df['apellido_materno'] + ' ' + df['nombres']
    df = df.drop(['apellido_materno', 'apellido_paterno', 'nombres'], axis = 1)
    #name_data = df['nombre_completo'].apply(separate_name)
    #df = pd.concat([df.drop(['nombre_completo'], axis=1), name_data.apply(pd.Series)], axis=1)
    
    df['plantel'] = df['matricula'].apply(get_plantel)

    #print(df.head())
    dict = df.to_dict('records')
    return dict
