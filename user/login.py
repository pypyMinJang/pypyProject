import sqlite3
import getpass

from . import user
from . import CONSTANT as const

def login(id, pw):
    return user.User(id, pw)
def logout():
    return
def signing():
    conn = sqlite3.connect(const._DB_URI)
    cur = conn.cursor()

    conn.execute("CREATE TABLE if not exists users(\
    id TEXT, pw TEXT, checked TEXT)")

    while True:
        id = input('id : ')
        pw = getpass.getpass('pw : ')
        cur.execute('SELECT * FROM users WHERE id = ? ', (id, ))

        if cur.fetchone():
            print('this id is already exist')
        else:
            break
    
    cur.execute('INSERT INTO users VALUES (?, ?, ?)', (id, pw, ''))

    conn.commit()
    
    return
def delete():
    return