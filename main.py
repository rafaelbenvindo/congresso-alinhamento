from pathlib import Path
from datetime import date

CONFIG_FILE = 'conf/config.json'
DATA_DIR = 'data'


def download_file(url, filename):
    import urllib.request as request
    print(f'Baixando arquivo {url} ...')
    request.urlretrieve(url, filename)


def execute_sql(sql):
    print('Executando sql: ' + sql)


def recreate_table_from_csv(file):
    import re
    table_name = 'csv_' + re.search('\w+', file.name).group()
    with open(file, 'r', encoding='utf-8') as file:
        headers = file.readline().strip()
    print(f'Criando tabela {table_name} com headers {headers}...')
    headers = headers.replace('"', '').split(';')
    fields = ','.join(([field + ' VARCHAR(5000)' for field in headers]))
    create_table_sql = f'DROP TABLE IF EXISTS {table_name};CREATE TABLE {table_name} ({fields});'
    execute_sql(create_table_sql)


def import_file(url):
    today = date.today()
    url = url.format(today.year)
    filepath = Path(DATA_DIR) / Path(url).name
    if filepath.exists():
        filedate = date.fromtimestamp(filepath.stat().st_mtime)
    else:
        filedate = None

    if today != filedate:
        download_file(url, filepath)
        recreate_table_from_csv(filepath)
    else:
        print(f'Arquivo {filepath.name} está com data de hoje, não será baixado.')


def create_dir(dirname):
    Path(dirname).mkdir(exist_ok=True)


def initial_setup():
    create_dir(DATA_DIR)


def import_congress_files():
    import json

    initial_setup()
    data_files = json.load(open(CONFIG_FILE))
    for f in data_files['files']:
        import_file(f['file'])


if __name__ == '__main__':
    import_congress_files()
