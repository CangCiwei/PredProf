import requests

def read_token(path):
    """ извлечение токена """
    with open(path) as fd:
        token = fd.read()
    return token

def load_data(url, token):
    """ извлечение данных """
    data = None
    try:
        res=requests.get(url, headers={"X-Auth-Token": token})
        if res.status_code == 200:
            data = res.json()
    except Exeption:
        pass
    return data
