from datetime import datetime

from requests import get
from requests import post

from bs4 import BeautifulSoup


# Credentials
username = "kamaletdinovaym"
password = "v2wsng68"

start_datetime = datetime.now()


# Authentication
response_on_get_page = get(url="https://cas.kai.ru:8443/cas/login")

token_JSESSIONID = response_on_get_page.cookies["JSESSIONID"]

page = response_on_get_page.text
parsed_page = BeautifulSoup(page, features="html.parser")
input_lt = parsed_page.find(name="input", attrs={ "name": "lt" })

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

print(datetime.now() - start_datetime, token_LT, "|", token_JSESSIONID)
start_datetime = datetime.now()


# Authorisation
token_CASTGC = response_on_authenticate.cookies["CASTGC"]

response_on_cas = get(
    url="https://cas.kai.ru:8443/cas/login?service=https://kai.ru/c/portal/login",
    headers={
        "Cookie": "CASTGC={token}".format(token=token_CASTGC),
    }
)

print(datetime.now() - start_datetime, token_CASTGC)
start_datetime = datetime.now()


# Getting needed data
token_JSESSIONID = response_on_cas.history[1].cookies["JSESSIONID"]

print(datetime.now() - start_datetime, token_JSESSIONID)
start_datetime = datetime.now()

data_type = "attestacia" #"raspisanie"

response_on_kai = get(
    url=f"https://kai.ru/group/guest/student/{data_type}",
    headers={
        "Cookie": "JSESSIONID={token}".format(token=token_JSESSIONID)
    }
)

print(datetime.now() - start_datetime, response_on_kai.text.strip()[-144:-30])

# "https://kai.ru/group/guest/student/attestacia?p_auth=im4UNXU5&p_p_id=myBRS_WAR_myBRS10&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_myBRS_WAR_myBRS10_javax.portlet.action=selectSemester&semester=4"
