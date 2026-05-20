import requests

URL = "http://127.0.0.1:8000/hello"

allowed = 0
blocked = 0

for i in range(15):
    r = requests.get(URL)
    if r.status_code == 200:
        allowed += 1
    elif r.status_code == 429:
        blocked += 1
    print(i+1, r.status_code)

print("Allowed:", allowed)
print("Blocked:", blocked)