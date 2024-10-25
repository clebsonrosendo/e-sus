import psycopg2 as psy
import json
import pandas as pd
import time
import datetime
import pdfkit

FILE = 'secrets_db.json'
PARTH_REPORT = './layout_report/'


# Create and getting file
def create_settings_file():
    dictionary = {
        'host': '',
        'port': '',
        'database': '',
        'username': '',
        'password': '',
        'date': ''
    }

    with open(FILE, 'w') as file:
        json.dump(dictionary, file)

    return

def get_settings_file():
    while True:
        try:
            with open(FILE, 'r') as file:
                data = json.load(file)
            break
        except FileNotFoundError:
            create_settings_file()

    return data


# Established connection
def connection_database():
    data = get_settings_file()

    DB_NAME = data['database']
    DB_USER = data['username']
    DB_PASS = data['password']
    DB_HOST = data['host']
    DB_PORT = data['port']

    connection = psy.connect(database=DB_NAME,
                             user=DB_USER,
                             password=DB_PASS,
                             host=DB_HOST,
                             port=DB_PORT)
    return connection


# Query
def query_database():
    df = None
    connection = connection_database()

    try:
        with open('query.sql', 'r') as file:
            query = str(file.read())

        cursor = connection.cursor()
        cursor.execute(query)

    except IOError:
        with open('query.sql', 'w') as file:
            query = file.write('Insert your query here')
    else:
        df = cursor.fetchall()
        connection.close()
        return df


# Make Dataframe with Query
def make_df():
    data = query_database()
    file = get_settings_file()
    date = file['date']

    df = pd.DataFrame(data)
    df = df.rename(columns={0: 'Data',
                            1: 'Profissional CNS',
                            2: 'Profissional Nome',
                            3: 'Paciente Nome',
                            4: 'Paciente_CNS',
                            5: 'Procedimentos'})
    # df = df[df['Data'] == date]

    return df


# Formatting Dataframe
def transform_data(df, key):
    # Get data
    df = pd.DataFrame(df)
    df = df[df["Profissional CNS"] == key]

    date = df.loc[:, 'Data'].unique()
    profissional_cns = df.loc[:, 'Profissional CNS'].unique()
    profissional_nome = df.loc[:, 'Profissional Nome'].unique()

    pacientes_total = df.loc[:, 'Paciente_CNS'].nunique()
    procedimentos_total = len(df.index)

    df = df[['Data', 'Paciente Nome', 'Paciente_CNS', 'Procedimentos']]
    df = df.rename(columns={'Paciente Nome': 'Pacientes', 'Paciente_CNS': 'CNS', 'Procedimentos': 'Procedimento'})
    df = df.fillna(' ')

    # Passer HTML
    file_content = ''
    with open(f'{PARTH_REPORT}content.html', 'r') as file:
        file_content = file.read()
        file.close()

    file_content = file_content.replace('#profissional_name', str(profissional_nome[0]))
    file_content = file_content.replace('#day_date', str(date[0]))
    file_content = file_content.replace('#profissional_cns', str(profissional_cns[0]))
    file_content = file_content.replace('#pacientes_total_number', str(pacientes_total))
    file_content = file_content.replace('#procedimentos_total_number', str(procedimentos_total))

    df = df.to_html(classes='table_pacientes', index=False, justify='center', border=0)

    file_content = file_content.replace('#pacientes', df)

    return file_content


def generate_report():
    df = make_df()
    content = ''
    page = ''
    for value in df["Profissional CNS"].unique():
        values = transform_data(df, value)
        content += values

    with open(f'{PARTH_REPORT}index.html', 'r') as file:
        page = file.read()
        file.close()

    page = page.replace('#conteudo', str(content))

    return page


def save_pdf():
    options = {
        'encoding': "UTF-8",
        'enable-local-file-access': "",
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'dpi': '300',
        'footer-right': '[page]',
        'print-media-type': '',
        'keep-relative-links': ''
    }

    # Date and time
    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

    report = generate_report()
    pdfkit.from_string(report, f'.\reports\Relatorio de Profissionais_{dt}.pdf', options=options)

    return


if __name__ == '__main__':
    save_pdf()
