import requests


def get_dog_photo() -> str:
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    return data["message"] if data["status"] == "success" else "No photo found"
