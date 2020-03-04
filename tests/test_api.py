import http
import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import requests_mock

from chart_museum_cleaner.api import BASE_URL, api, charts, list_all_charts, delete_chart_version

TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'


@pytest.fixture()
def list_charts_response():
    with open(f'{TEST_DATA_DIR}/list-charts-response.json') as json_file:
        response = json.load(json_file)
        return response


def test_list_all_charts(list_charts_response):
    with requests_mock.mock() as m:
        m.get(f'{BASE_URL}/{api}/{charts}', json=list_charts_response)
        response = list_all_charts()

        assert response == list_charts_response


@pytest.fixture()
def mock_os(monkeypatch):
    mock_os = MagicMock()
    monkeypatch.setattr('chart_museum_cleaner.api.os', mock_os)
    return mock_os


def test_delete_chart_version_given_token(monkeypatch):
    name = 'test'
    version = '1.0'
    token = 'test-token'
    monkeypatch.setenv('TOKEN', token)

    with requests_mock.mock() as m:
        m.delete(f'{BASE_URL}/{api}/{charts}/{name}/{version}',
                 headers={'Authorization': f'Bearer {token}'},
                 status_code=200)
        resp = delete_chart_version(name, version)
        assert resp.status_code == http.HTTPStatus.OK


def test_delete_chart_version_given_no_token():
    name = 'test'
    version = '1.0'
    with requests_mock.mock() as m:
        m.delete(f'{BASE_URL}/{api}/{charts}/{name}/{version}', status_code=200)
        resp = delete_chart_version(name, version)
        assert resp.status_code == http.HTTPStatus.OK
