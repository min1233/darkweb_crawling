import requests
from bs4 import BeautifulSoup
import re

search_url = "https://onionsearchengine.com/search.php?search=TEST&submit=Search&page="

http_list = []

def get_http(a_tag):
    global http_list
    http_re = "http[s]?:\/\/[a-zA-Z0-9\.]*\.onion\/"
    for tag in a_tag:
        tmp = re.findall(http_re,str(tag))
        if(tmp!=[]):
            http_list.append(tmp[0])
    return list(set(http_list))

session = requests.session()

session.proxies = {
        "http":"socks5h://127.0.0.1:9050",
        "https":"socks5h://127.0.0.1:9050",
}

if __name__ == "__main__":
    for i in range(1,20):
        rep = requests.get(search_url.replace("TEST","gun")+str(i))
        if(rep.text.find("Sorry, there are no matching result fo")!=-1):
            print("Search END")
            break
        else:
            bs = BeautifulSoup(rep.text, 'html.parser')
            a_tag = bs.select('a')
            http_list = get_http(a_tag)

    for http in http_list:
        print(http)
