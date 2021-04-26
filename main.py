import requests

url = "http://myipaddress.com"
proxies = {
        "http":"socks5://127.0.0.1:9050",
        "https":"socks5://127.0.0.1:9050",
}

rep = requests.get(url, proxies = proxies)

print(rep.text)
