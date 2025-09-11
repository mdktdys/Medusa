from http import HTTPStatus

import httpx
import requests


def get_remote_file_bytes(link: str) -> bytes:
    response: requests.Response = requests.get(link)
    if response.status_code == HTTPStatus.OK.value:
        return response.content
    else:
        raise Exception("Данные не получены")
    
    
async def get_remote_file_bytes_async(url: str) -> bytes | None:
    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"}
        ) as client:
            resp = await client.get(url)
            if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("image/"):
                return resp.content
            else:
                print(
                    "Download failed",
                    {"status": resp.status_code, "ctype": resp.headers.get("Content-Type"),
                     "history": [f"{h.status_code} {h.headers.get('Location')}" for h in resp.history]}
                )
    except Exception as e:
        print(f"Ошибка при скачивании фото: {e}")
    return None