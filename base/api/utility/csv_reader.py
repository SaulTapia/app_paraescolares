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

def file_to_students(file):
    df = pd.read_csv(file, index_col=False)
    
    print(df.head())
    
    df.columns = ['nombre_completo', 'grupo' 'matricula']
    
    df['turno'] = df['grupo'].apply(make_turn)

    for column in ['nombre_completo']:
        df[column] = df[column].apply(remove_accents).str.upper()

    dict = df.to_dict('records')
    return dict
