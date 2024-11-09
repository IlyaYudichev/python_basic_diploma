import requests
from config_data.config import KINOPOISK_API_KEY

def api_request(method_endswith,
                params
                ):
    url = f"https://api.kinopoisk.dev/{method_endswith}"

    try:
        response = requests.get(
            url,
            headers={"accept": "application/json",
	                 "X-API-KEY": KINOPOISK_API_KEY
	        },
            params=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.json()
    except:
        pass
