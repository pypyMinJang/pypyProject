import sqlite3

from . import CONSTANT as const

class User:
    def __init__(self, id='guest', pw='guest'):
        conn = sqlite3.connect(const._DB_URI)
        cur = conn.cursor()

        conn.execute("CREATE TABLE if not exists users(\
        id TEXT, pw TEXT, checked TEXT)")
        cur.execute('SELECT * FROM users WHERE id = ? AND pw = ?', (id, pw))

        if cur.fetchone() :
            self.id = id
            self.pw = pw
        else :
            print('login failed login with guest')
        

