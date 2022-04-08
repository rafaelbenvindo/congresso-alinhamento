import json
from pathlib import Path
from datetime import date

DATA_DIR = 'data'


def download_file(url, filename):
    import urllib.request as request
    ano_atual = date.today().year
    url = url.format(ano_atual)
    print(f'Baixando arquivo {url} ...')
    request.urlretrieve(url, filename)


def execute_sql(sql):
    print('Executando sql: ' + sql)


def create_table_from_csv(table_name, headers):
    table_name = 'csv_' + table_name
    print(f'Criando tabela {table_name} com headers {headers}...')
    headers = headers.replace('"', '').split(';')
    fields = ','.join(([field + ' VARCHAR(5000)' for field in headers]))
    create_table_sql = f'CREATE TABLE {table_name} ({fields});'
    execute_sql(create_table_sql)


def import_file(url):
    import re
    filepath = Path(DATA_DIR) / Path(url).name
    download_file(url, filepath)
    table_name = re.search('\w+', filepath.name).group()
    with open(filepath, 'r', encoding='utf-8') as file:
        headers = file.readline().strip()
    create_table_from_csv(table_name, headers)


def create_dir(dirname):
    Path(dirname).mkdir(exist_ok=True)


def initial_setup():
    create_dir(DATA_DIR)


if __name__ == '__main__':
    initial_setup()
    data_files = json.load(open('conf\\urls.json'))
    for f in data_files['files']:
        import_file(f['file'])
