import requests
import json
from my_secrets import OPENROUTER_API_KEY

extract_groups_promt: str = 'Напиши списком через запятую группы которые на практике. Учти, что запись  21СА-1,2 это имеется ввиду 21СА-1 и 21СА-2 и написать их надо отдельно. Не пиши ничего лишнего кроме групп'


def send_ai_request(request: str):
    response: requests.Response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    },
    data = json.dumps({
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [
        {
            "role": "user",
            "content": f"{request}"
        }
        ]
    })
    )
    
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']