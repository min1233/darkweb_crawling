import pymysql

class mysql:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='darkweb', password='password', db='darkweb', charset='utf8')
        self.cursor = self.conn.cursor()

    def insert_data(self, url, title, file_path):
        sql = "INSERT INTO onion_url (url, title, file_path, search_time) VALUES (%s, %s, %s, NOW())"
        self.cursor.execute(sql, (url,title,file_path))
        self.conn.commit()

    def select_data(self, url):
        sql = "select url from onion_url WHERE url=%s"
        self.cursor.execute(sql, (url))
        rows = self.cursor.fetchone()
        return rows

    def close(self):
        self.conn.close()
