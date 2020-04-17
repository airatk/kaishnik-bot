
# Logging in from `cas.kai.ru`

### `cURL`
    curl 'https://cas.kai.ru:8443/cas/login' \
    -XPOST \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Origin: https://cas.kai.ru:8443' \
    -H 'Cookie: JSESSIONID=EC5853D38A87BED7A36195D51D7F1F72; _ga=GA1.2.822234025.1578790427; _gid=GA1.2.600909276.1980238766; _ym_visorc_23188831=w; p1="rjGyDFfzS9QlyKzfoYt58g=="; p2="RABZMmaJ7HhNF+xnsHqOPA=="; COMPANY_ID=10154; ID=4237473869596677504a98785a69724c7748454f47773d3d; _ym_isad=2; _ym_d=1580120455; _ym_uid=1573985244654408728' \
    -H 'Content-Length: 155' \
    -H 'Accept-Language: en-au' \
    -H 'Host: cas.kai.ru:8443' \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15' \
    -H 'Referer: https://cas.kai.ru:8443/cas/login' \
    -H 'Connection: keep-alive' \
    --data 'username=username&password=password&lt=LT-198475-J3OmEi1gb2Q1IBjV3oNRDE34yz0iz4&execution=e1s1&_eventId=submit&submit=%D0%92%D0%9E%D0%99%D0%A2%D0%98'

### `POST` data
    username: username
    password: password
    lt: LT-667-jt4lbDvNggkSTyi3cAAbYLbKeZWY22
    execution: e1s1
    _eventId: submit
    submit: ВОЙТИ


### Request headers

    POST /cas/login HTTP/1.1
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Content-Type: application/x-www-form-urlencoded
    Origin: https://cas.kai.ru:8443
    Cookie: JSESSIONID=EC5853D38A12ADE7A36195D51D7F1F64; _ga=GA1.2.822058325.1578490427; _gid=GA1.2.600629676.1599178766; _ym_visorc_23188831=w; p1="rjGyDFaeS9QlyKzfoL3I8g=="; p2="MCEZMmaJ7EhND+xnsHqOPA=="; COMPANY_ID=10154; ID=4237473869567147504a61385a69724c7748454f47773d3d; _ym_isad=2; _ym_d=1580120455; _ym_uid=1573985244654408728
    Content-Length: 155
    Accept-Language: en-au
    Host: cas.kai.ru:8443
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15
    Referer: https://cas.kai.ru:8443/cas/login
    Accept-Encoding: gzip, deflate, br
    Connection: keep-alive


### Response headers

    HTTP/1.1 200 OK
    Set-Cookie: CASPRIVACY=""; Expires=Thu, 01-Jan-1970 00:00:10 GMT; Path=/cas/, CASTGC=TGT-12868-BJB9dUP9Bc2tERIAs7m1uwAvWG9I0DklO9dNqXfjJGtRPdewBc-cas.kai.ru; Path=/cas/; Secure
    Content-Type: text/html;charset=UTF-8
    Pragma: no-cache
    Date: Thu, 30 Jan 2020 19:43:56 GMT
    Content-Length: 1938
    Expires: Thu, 01 Jan 1970 00:00:00 GMT
    Cache-Control: no-cache, no-store
    Server: Apache-Coyote/1.1


# `cas.kai.ru:8443/cas/login` page

## Cleaned login `form`

    <form action="/cas/login" method="post">
            <div>
                <input name="username" type="text" />
            </div>
            
            <div>
                <input name="password" type="password" />
            </div>
            
            <div>
                <input name="warn" value="true" type="checkbox" />
            </div>
            
            <div>
                <input type="hidden" name="lt" value="LT-133-Evqx7fWbeE4SAbc1uzMyDHVq0aiNap" />
                <input type="hidden" name="execution" value="e1s1" />
                <input type="hidden" name="_eventId" value="submit" />

                <input name="submit" value="ВОЙТИ" type="submit" />
                <input name="reset" value="ОЧИСТИТь" type="reset" />
            </div>
    </form>


## Full login `form`

    <form id="fm1" class="fm-v clearfix" action="/cas/login" method="post">
        <!-- Поздравляем с успешным запуском системы CAS! "Authentication handler", установленный по умолчанию, производит установление подлинности в том случае если имя пользователя и пароль совпадают: попробуйте систему CAS в действии. -->
            <h2>Введите логин и пароль.</h2>
            
            <div class="row fl-controls-left">
                <label for="username" class="fl-label">Логин:</label>
                <input id="username" name="username" class="required" tabindex="1" accesskey="n" type="text" value="" size="25" autocomplete="false"/>
            </div>
            
            <div class="row fl-controls-left">
                <label for="password" class="fl-label"><span class="accesskey">П</span>ароль:</label>
                <input id="password" name="password" class="required" tabindex="2" accesskey="p" type="password" value="" size="25" autocomplete="off"/>
            </div>
            
            <div class="row check">
                <input id="warn" name="warn" value="true" tabindex="3" accesskey="п" type="checkbox" />
                <label for="warn"><span class="accesskey">П</span>редупредить перед входом на другие сайты.</label>
            </div>
            
            <div class="row btn-row">
                <input type="hidden" name="lt" value="LT-133-Evqx7fWbeE4SAbc1uzMyDHVq0aiNap" />
                <input type="hidden" name="execution" value="e1s1" />
                <input type="hidden" name="_eventId" value="submit" />

                <input class="btn-submit" name="submit" accesskey="l" value="ВОЙТИ" tabindex="4" type="submit" />
                <input class="btn-reset" name="reset" accesskey="c" value="ОЧИСТИТь" tabindex="5" type="reset" />
            </div>
    </form>


# Some tokens

- `LT`: login token? - purpose is unknown, located in hidden `<input>` tag on `cas.kai.ru:8443/cas/login` page
- `CASTGT`: ticket granting token - purpose is not clear, seems like it's used to authorise a user on `cas.kai.ru` page, located in `response` cookies when login credentials are `post`ed
- `ST`: service token - purpose is not clear, seems like it's used to authorise a user on `kai.ru`, seems like it's given by the server
- `JSESSIONID`: session id - user is authorised on `kai.ru` by this cookie value 


# Some links

- `https://cas.kai.ru:8443/cas/login?service=https://kai.ru/c&auto=true`
- `https://cas.kai.ru:8443/cas/login?service=https%3A%2F%2Fkai.ru%2Fc%2Fportal%2Flogin`
- `https://cas.kai.ru:8443/cas/login?service=https://kai.ru/c/portal/login`
- `https://kai.ru/c?ticket=ST-57258-dyxlPAcCeVEdgkYvNiAq-cas.kai.ru`


# Scanning ports of `kai.ru` IP

    Nmap scan report for 193.105.65.13
    Not shown: 996 filtered ports
    PORT     STATE  SERVICE
    80/tcp   open   http
    113/tcp  closed ident
    443/tcp  open   https
    8443/tcp open   https-alt
