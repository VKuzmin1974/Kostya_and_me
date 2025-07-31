import requests

URL = "https://restcountries.com/v3.1/name/{}"


def get_country_info(country_name: str):
    response = requests.get(URL.format(country_name)).json()
    if isinstance(response, dict):
        return None
    return {
        'capital': response[0]['capital'][0],
    }


print(get_country_info('russia'))

