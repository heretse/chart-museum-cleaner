import http

import click

from .api import delete_chart_version


def get_name_and_versions_to_delete(chart_response, keep=2):
    """
    Get name and unused versions from chart api response. Please see test if confusing about the input and output.
    If less than 1 to keep, return empty empty to delete
    :param chart_response: api response of charts
    :param keep: number of versions to keep. default only keep one
    :return: Dict(str, list) contains chart name and versions
    """
    name_and_versions = dict()

    if keep < 1:
        return name_and_versions

    for k, v in chart_response.items():
        name_and_versions[k] = list()
        count = 0

        for value in v:
            if count >= keep:
                name_and_versions[k].append(value['version'])
            else:
                count += 1
    return name_and_versions


def delete_name_and_versions(name_and_versions):
    """
    Call the endpoint to delete unused charts
    :param name_and_versions: Dict(str, list) which stores chart name and its versions in list
    :return:
    """
    for name, versions in name_and_versions.items():
        for version in versions:
            click.echo(f'Will remove chart: {name}, version: {version}')
            resp = delete_chart_version(name, version)

            if resp.status_code == http.HTTPStatus.OK:
                click.echo(f'Removed chart: {name}, version: {version}')
            else:
                click.echo(f"Fail to delete chart: {name}, version: {version}, "
                           f"status: {resp.status_code}, reason: {resp.reason}", color='red')
