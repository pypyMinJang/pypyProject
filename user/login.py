import sqlite3
import getpass

from . import user
from . import CONSTANT as const

def login(id, pw):
    return user.User(id, pw)
def signing():
    conn = sqlite3.connect(const._DB_URI)
    cur = conn.cursor()

    conn.execute("CREATE TABLE if not exists users(\
    id TEXT, pw TEXT, checked TEXT)")

    while True:
        id = input('id : ')
        while id == '' or id == 'guest' or ' ' in id or '\t' in id:
            print("without blank or 'guest' write something..")
            if input('give up?(Y/N) ') == 'Y':
                conn.close()
                return False
            else :
                id = input('id : ')

        pw = getpass.getpass('pw : ')
        while pw == '' or ' ' in pw or '\t' in pw:
            print('without blank write something..')
            if input('give up?(Y/N) ') == 'Y':
                conn.close()
                return False
            else :
                pw = getpass.getpass('pw : ')

        cur.execute('SELECT * FROM users WHERE id = ? ', (id, ))

        if cur.fetchone():
            print('this id is already exist')
            if input('give up?(Y/N) ') == 'Y':
                conn.close()
                return False              
        else:
            cur.execute('INSERT INTO users VALUES (?, ?, ?)', (id, pw, ''))
            conn.commit()
            return True
