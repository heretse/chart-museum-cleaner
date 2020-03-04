import http
import json
from pathlib import Path
from unittest.mock import MagicMock, call

import pytest

from chart_museum_cleaner import cleaner

TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'


@pytest.fixture()
def list_charts_response():
    with open(f'{TEST_DATA_DIR}/list-charts-response.json') as json_file:
        response = json.load(json_file)
        return response


def test_get_name_and_versions_to_delete_given_one_to_keep(list_charts_response):
    result = cleaner.get_name_and_versions_to_delete(list_charts_response, 1)
    expected = {"order-service": [],
                "shipment-service": ["1.0.51525", "1.0.49554", "1.0.49299"]}
    assert result == expected


def test_get_name_and_versions_to_delete_given_three_to_keep(list_charts_response):
    result = cleaner.get_name_and_versions_to_delete(list_charts_response, 3)
    expected = {"order-service": [],
                "shipment-service": ["1.0.49299"]}
    assert result == expected


def test_get_name_and_versions_to_delete_given_zero_to_keep(list_charts_response):
    result = cleaner.get_name_and_versions_to_delete(list_charts_response, 0)
    expected = dict()
    assert result == expected


@pytest.fixture()
def mock_delete_chart_version(monkeypatch):
    mock_delete_chart_version = MagicMock()
    monkeypatch.setattr('chart_museum_cleaner.cleaner.delete_chart_version', mock_delete_chart_version)
    return mock_delete_chart_version


@pytest.fixture()
def mock_click(monkeypatch):
    mock_click = MagicMock()
    monkeypatch.setattr('chart_museum_cleaner.cleaner.click', mock_click)
    return mock_click


def test_delete_name_and_versions_given_status_code_ok(mock_delete_chart_version, mock_click):
    name_and_versions = {'test': ['3', '2', '1'], 'test-x': ['2.1']}
    resp = MagicMock()
    resp.status_code = http.HTTPStatus.OK
    mock_delete_chart_version.return_value = resp

    cleaner.delete_name_and_versions(name_and_versions)

    assert mock_delete_chart_version.call_args_list == [
        call('test', '3'), call('test', '2'), call('test', '1'), call('test-x', '2.1')]

    assert mock_click.echo.call_args_list == [call('Will remove chart: test, version: 3'),
                                              call('Removed chart: test, version: 3'),
                                              call('Will remove chart: test, version: 2'),
                                              call('Removed chart: test, version: 2'),
                                              call('Will remove chart: test, version: 1'),
                                              call('Removed chart: test, version: 1'),
                                              call('Will remove chart: test-x, version: 2.1'),
                                              call('Removed chart: test-x, version: 2.1')]


def test_delete_name_and_versions_given_status_code_not_ok(mock_delete_chart_version, mock_click):
    name_and_versions = {'test': ['3', '2', '1'], 'test-x': ['2.1']}

    resp = MagicMock()
    mock_delete_chart_version.return_value = resp
    resp.status_code = http.HTTPStatus.FORBIDDEN
    resp.reason = 'Permission denied'

    cleaner.delete_name_and_versions(name_and_versions)

    assert mock_click.echo.call_args_list == [call('Will remove chart: test, version: 3'),
                                              call(f'Fail to delete chart: test, version: 3, '
                                                   f'status: 403, reason: Permission denied', color='red'),
                                              call('Will remove chart: test, version: 2'),
                                              call('Fail to delete chart: test, version: 2, status: 403, '
                                                   'reason: Permission denied',
                                                   color='red'),
                                              call('Will remove chart: test, version: 1'),
                                              call('Fail to delete chart: test, version: 1, status: 403, '
                                                   'reason: Permission denied',
                                                   color='red'),
                                              call('Will remove chart: test-x, version: 2.1'),
                                              call('Fail to delete chart: test-x, version: 2.1, status: 403, '
                                                   'reason: Permission denied',
                                                   color='red')]
