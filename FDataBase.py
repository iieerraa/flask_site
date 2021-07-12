import math
import re
import time
import sqlite3
from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Ошибка чтения из БД')
        return []

    def add_post(self, title, text, url):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM post WHERE url LIKE "{url}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Статья с таким URL уже существует')
                return False

            base = url_for('static', filename='images')

            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>"+base+"/\\g<url>>",
                          text)

            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO post VALUES(NULL, ?, ?, ?, ?)', (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД ' + str(e))
            return False
        return True

    def get_post(self, alias):
        try:
            self.__cur.execute('SELECT title, text FROM post WHERE url LIKE ? LIMIT 1', (alias,))
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из БД ' + str(e))
        return (False, False)

    def get_post_anonce(self):
        try:
            self.__cur.execute('SELECT id, title, text, url FROM post ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из БД ' + str(e))
        return []
