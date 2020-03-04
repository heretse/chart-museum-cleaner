from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

from chart_museum_cleaner.cli import cli


@pytest.fixture()
def mock_list_charts(monkeypatch):
    mock_list_charts = MagicMock()
    monkeypatch.setattr('chart_museum_cleaner.cli.list_all_charts', mock_list_charts)
    return mock_list_charts


@pytest.fixture()
def mock_get_name_and_versions_to_delete(monkeypatch):
    mock_get_name_and_versions_to_delete = MagicMock()
    monkeypatch.setattr('chart_museum_cleaner.cli.get_name_and_versions_to_delete', mock_get_name_and_versions_to_delete)
    return mock_get_name_and_versions_to_delete


@pytest.fixture()
def mock_delete_name_and_versions(monkeypatch):
    mock_delete_name_and_versions = MagicMock()
    monkeypatch.setattr('chart_museum_cleaner.cli.delete_name_and_versions', mock_delete_name_and_versions)
    return mock_delete_name_and_versions


def test_delete_unused_versions_given_zero_to_keep(mock_list_charts, mock_get_name_and_versions_to_delete,
                                                   mock_delete_name_and_versions):
    runner = CliRunner()

    result = runner.invoke(cli, ['delete', '--keep', 0])

    mock_list_charts.assert_not_called()
    mock_get_name_and_versions_to_delete.assert_not_called()
    mock_delete_name_and_versions.assert_not_called()

    assert not result.exception
    assert result.exit_code == 0


def test_delete_unused_versions(mock_list_charts, mock_get_name_and_versions_to_delete,
                                mock_delete_name_and_versions):
    runner = CliRunner()

    result = runner.invoke(cli, ['delete'])

    mock_list_charts.assert_called_once()
    mock_get_name_and_versions_to_delete.assert_called_once()
    mock_delete_name_and_versions.assert_called()

    assert not result.exception
    assert result.exit_code == 0
