import mysqllib as mysql_class
import requests
import re
import os
import threading
from datetime import datetime
from bs4 import BeautifulSoup

search_url = "https://onionsearchengine.com/search.php?search=TEST&submit=Search&page="
# onion Search Engine
#search_url2 = "http://visitorfi5kl7q7i.onion/search/?q=TEST&page="
session = requests.session()

# color
bold = "\033[1m"
end = "\033[0m"

session.proxies = {
        "http":"socks5h://127.0.0.1:9050",
        "https":"socks5h://127.0.0.1:9050",
}

# find onion Link
def get_http_link(a_tag, http_list):
    http_re = "http[s]?:\/\/[a-zA-Z0-9\.]*\.onion\/"
    for tag in a_tag:
        tmp = re.findall(http_re,str(tag))
        if(tmp!=[]):
            http_list.append(tmp[0])
    return list(set(http_list))

# search for keyword at onionsearchengine.com
def search_keyword(keyword, mysql, index=100):
    http_list = []
    for i in range(1, index):
        if(i%100==0):
            print(f"{i} / {index}")
        rep = requests.get(search_url.replace("TEST",keyword)+str(i))
        if(rep.text.find("Sorry, there are no matching result fo")!=-1):
            print("Search END")
            break
        else:
            bs = BeautifulSoup(rep.text, 'html.parser')
            a_tag = bs.select('a')
            http_list = get_http_link(a_tag, http_list)
    for http in http_list:
        if(detect_stored_url(http, mysql)==1):
            http_list.remove(http)
    print(f"Keyword : {keyword}, Found {len(http_list)} onion")
    return http_list

# access onion url in http list
def find_onion(keyword, http_list, mysql):
    count = 1;
    dir_path = "./data/"+datetime.today().strftime("%Y_%m_%d")+"/"+keyword
    os.system(f"mkdir -p {dir_path}")
    for url in http_list:
        try:
            rep = session.get(url, timeout=5)
            bs = BeautifulSoup(rep.text, 'html.parser')
            
            title = bs.select_one('title').text.strip()
            file_path = dir_path+"/"+str(count)+".html"
            print(f"{bold}[{keyword}]{end} Find Title : {title}")
            
            mysql.insert_data(url, title, file_path)

            f = open(file_path,"w")
            f.write(rep.text)
            f.close()            

            # get onion url in html code
            bs = BeautifulSoup(rep.text, 'html.parser')
            a_tag = bs.select('a')
            tmp_list = get_http_link(a_tag, [])
            
            # Find new onion url without duplication
            for tmp in tmp_list:
                if tmp not in http_list:
                    if(detect_stored_url(tmp, mysql)==0):
                        http_list.append(tmp)
            count += 1;

        # Add to Database Unconnectable onion url
        except Exception as e:
            mysql.insert_data(url, "-", "-")
#            print(e);
            continue

# Discriminate new onion url
def detect_stored_url(url, mysql):
    data = mysql.select_data(url)
    if(data!=None):
        return 1
    else:
        return 0

# main thread function
def main_fun(keyword, index, mysql):
    http_list = search_keyword(keyword, mysql, index)
    find_onion(keyword, http_list, mysql)

if __name__ == "__main__":
    keyword_list = ["sex", "account","credit card"]
    mysql = mysql_class.mysql()
    # search keyword
    for keyword in keyword_list:
        main_fun(keyword, 1000, mysql);
    mysql.close()
#    t = threading.Thread(tarrget=keyword_search, args=["gun",100])
#    t.start()
