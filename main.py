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
def search_keyword(keyword, index=100):
    http_list = []
    for i in range(1, index):
        rep = requests.get(search_url.replace("TEST",keyword)+str(i))
        if(rep.text.find("Sorry, there are no matching result fo")!=-1):
            print("Search END")
            break
        else:
            bs = BeautifulSoup(rep.text, 'html.parser')
            a_tag = bs.select('a')
            http_list = get_http_link(a_tag, http_list)
    print(f"Keyword : {keyword}, Found",len(http_list),"onion")
    return http_list

# access onion url in http list
def find_onion(keyword, http_list):
    count = 0;
    dir_path = "./data/"+datetime.today().strftime("%Y_%m_%d")+"/"+keyword
    os.system(f"mkdir -p {dir_path}")
    for url in http_list:
        try:
            rep = session.get(url)
            bs = BeautifulSoup(rep.text, 'html.parser')
            
            title = bs.select_one('title').text
            file_path = dir_path+"/"+str(count)+".html"
            print(f"{bold}[{keyword}]{end} Find Title : {title}")
            
            mysql = mysql_class.mysql()
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
                    http_list.append(tmp)
            count += 1;
        except Exception as e:
#            print(e);
            continue
    mysql.close()

# main thread function
def main_fun(keyword, index):
    http_list = search_keyword(keyword, index)
    find_onion(keyword, http_list)

if __name__ == "__main__":
    main_fun("gun", 100);
#    t = threading.Thread(tarrget=keyword_search, args=["gun",100])
#    t.start()
