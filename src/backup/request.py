import requests 

session = requests.session()

request_get = session.get("https://www.google.com")
print(request_get.text)