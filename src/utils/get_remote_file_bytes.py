from http import HTTPStatus

import requests


def get_remote_file_bytes(link: str) -> bytes:
    response: requests.Response = requests.get(link)
    if response.status_code == HTTPStatus.OK.value:
        return response.content
    else:
        raise Exception("Данные не получены")