import os

import requests

import base64

BASE_URL = os.getenv("CHART_MUSEUM_URL", "http://localhost:8080")
TOKEN = os.getenv('TOKEN', '')
USER = os.getenv('USER', '')

api = 'api'

charts = 'charts'


def list_all_charts():
    if USER:
        return requests.get(f'{BASE_URL}/{api}/{charts}',
                            headers={'Authorization': f'Basic {base64.b64encode(USER.encode("UTF-8")).decode("UTF-8")}'}
                            ).json()
    else:
        return requests.get(f'{BASE_URL}/{api}/{charts}').json()


def delete_chart_version(name, version):
    if TOKEN:
        return requests.delete(f'{BASE_URL}/{api}/{charts}/{name}/{version}',
                               headers={'Authorization': f'Bearer {TOKEN}'}
                               )
    elif USER:
        return requests.delete(f'{BASE_URL}/{api}/{charts}/{name}/{version}',
                               headers={'Authorization': f'Basic {base64.b64encode(USER.encode("UTF-8")).decode("UTF-8")}'}
                               )
    else:
        return requests.delete(f'{BASE_URL}/{api}/{charts}/{name}/{version}')
