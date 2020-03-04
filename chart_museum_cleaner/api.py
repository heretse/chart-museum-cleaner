import os

import requests

BASE_URL = os.getenv("CHART_MUSEUM_URL", "http://localhost:8080")
TOKEN = os.getenv('TOKEN', '')

api = 'api'

charts = 'charts'


def list_all_charts():
    return requests.get(f'{BASE_URL}/{api}/{charts}').json()


def delete_chart_version(name, version):
    if TOKEN:
        return requests.delete(f'{BASE_URL}/{api}/{charts}/{name}/{version}',
                               header={'Authorization': f'Bearer {TOKEN}'}
                               )
    else:
        return requests.delete(f'{BASE_URL}/{api}/{charts}/{name}/{version}')
