import requests

url = "http://gvka2m4qt5fod2fltkjmdk4gxh5oxemhpgmnmtjptms6fkgfzdd62tad.onion"
session = requests.session()

session.proxies = {
        "http":"socks5h://127.0.0.1:9050",
        "https":"socks5h://127.0.0.1:9050",
}

rep = session.get(url)

print(rep.text)
