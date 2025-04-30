import requests

API_KEY = "ak-d59ad68203ac4e75ba9f61eb0208789c"
USER_ID = "IMDBa26u92UeN8BKEw3J33LJk4R2"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "X-User-Id": USER_ID,
    "Content-Type": "application/json",
}

resp = requests.post("https://api.play.ht/api/v4/websocket-auth", headers=headers)
print(resp.status_code, resp.text)
