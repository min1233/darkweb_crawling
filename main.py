import mysqllib as mysql_class
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
import os

search_url = "https://onionsearchengine.com/search.php?search=TEST&submit=Search&page="

http_list = []

session = requests.session()

session.proxies = {
        "http":"socks5h://127.0.0.1:9050",
        "https":"socks5h://127.0.0.1:9050",
}

def get_http_link(a_tag):
    global http_list
    http_re = "http[s]?:\/\/[a-zA-Z0-9\.]*\.onion\/"
    for tag in a_tag:
        tmp = re.findall(http_re,str(tag))
        if(tmp!=[]):
            http_list.append(tmp[0])
    http_list = list(set(http_list))

def search_keyword(keyword, i=100):
    for i in range(1, i):
        rep = requests.get(search_url.replace("TEST",keyword)+str(i))
        if(rep.text.find("Sorry, there are no matching result fo")!=-1):
            print("Search END")
            break
        else:
            bs = BeautifulSoup(rep.text, 'html.parser')
            a_tag = bs.select('a')
            get_http_link(a_tag)

if __name__ == "__main__":
    dir_path = "./data/"+datetime.today().strftime("%Y_%m_%d")
    os.system(f"mkdir {dir_path}")
    search_keyword("gun", 100)
    for i, url in enumerate(http_list):
        try:
            rep = session.get(url)
            bs = BeautifulSoup(rep.text, 'html.parser')
            
            title = bs.select_one('title').text
            file_path = dir_path+"/"+str(i)+".html"
            
            mysql = mysql_class.mysql()
            mysql.insert_data(url, title, file_path)

            f = open(file_path,"w")
            f.write(rep.text)
            f.close()            
        except Exception as e:
            print(e)
            continue
