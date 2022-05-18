import sqlite3
import getpass
import datetime

from crawling.team import team_crawling
from crawling.schedule import scheduel_crawling
import user.login as login
import user.user as user
import CONSTANT as const

conn = sqlite3.connect(const._DB_URI)
cur = conn.cursor()
now = datetime.datetime.now()

cur.execute('SELECT * FROM updated WHERE type = ?', ('team', ))
lated = datetime.datetime.strptime(cur.fetchone()[1], '%Y-%m-%d %H:%M:%S.%f')
if (now-lated).days >= 1:
    team_crawling()

cur.execute('SELECT * FROM updated WHERE type = ?', ('schedule', ))
lated = datetime.datetime.strptime(cur.fetchone()[1], '%Y-%m-%d %H:%M:%S.%f')
if (now-lated).days >= 1:
    scheduel_crawling()

conn.close()

while True:
    signed = input('signed?(Y/N)')

    if signed == 'Y' :
        id = input('id : ')
        pw = getpass.getpass('pw : ')
        user = login.login(id, pw)
        break
    elif signed == 'N' :
        login.signing()
        id = input('id : ')
        pw = getpass.getpass('pw : ')
        user = login.login(id, pw)
        break
    else :
        print('?')



print("hello world!")