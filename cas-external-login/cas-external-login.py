from requests import get
from requests import post

from bs4 import BeautifulSoup


# Credentials
username = "username"
password = "password"


# Authentication
response_on_get_page = get(url="https://cas.kai.ru:8443/cas/login")

token_JSESSIONID = response_on_get_page.cookies["JSESSIONID"]

page = response_on_get_page.text
parsed_page = BeautifulSoup(page, features="html.parser")
input_lt = parsed_page.html.find(name="input", attrs={ "name": "lt" })

token_LT = input_lt["value"]

response_on_authenticate = post(
    url="https://cas.kai.ru:8443/cas/login",
    data={
        "username": username,
        "password": password,
        "execution": "e1s1",
        "_eventId": "submit",
        "lt": token_LT,
    },
    headers={
        "Cookie": "JSESSIONID={token}".format(token=token_JSESSIONID),
    }
)


# Authorisation
token_CASTGC = response_on_authenticate.cookies["CASTGC"]

response_on_cas = get(
    url="https://cas.kai.ru:8443/cas/login?service=https://kai.ru/c/portal/login",
    headers={
        "Cookie": "CASTGC={token}".format(token=token_CASTGC),
    }
)


# Getting the needed data
token_JSESSIONID = response_on_cas.history[1].cookies["JSESSIONID"]

response_on_kai = get(
    url="https://kai.ru/group/guest/student/raspisanie",
    headers={
        "Cookie": "JSESSIONID={token}".format(token=token_JSESSIONID)
    }
)

print("Headers:", response_on_kai.headers)
