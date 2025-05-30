import requests


def get_dog_fact() -> str:
    response = requests.get('https://dogapi.dog/api/facts')
    data = response.json()
    return data['facts'][0] if data['success'] else 'No facts found'
