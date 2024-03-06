import requests

url = "http://92.118.170.121/api/players/papa/"
headers = {
    "accept": "*/*",
    "accept-language": "ru,en;q=0.9",
    "content-type": "application/json",
    "x-csrftoken": "FWip7G6DafMVZr7yafSajvrAkfctAybU"
}
data = {"pos": 20}

response = requests.put(url, headers=headers, json=data, cookies={"Cookie": "your_cookie_value_here"})
print(response.status_code)
print(response.text)
