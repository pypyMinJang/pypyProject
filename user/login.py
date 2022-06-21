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
        id = input('사용할 아이디 : ')
        while id == '' or id == 'guest' or ' ' in id or '\t' in id:
            print("'guest'이외의 아이디로 공백 없이 작성해주세요..")
            if input('취소하시겠습니까?(Y/N) ') == 'Y':
                conn.close()
                return False
            else :
                id = input('사용할 아이디 : ')

        pw = getpass.getpass('사용할 비밀번호 : ')
        while pw == '' or ' ' in pw or '\t' in pw:
            print('공백 없이 작성해주세요..')
            if input('취소하시겠습니까?(Y/N) ') == 'Y':
                conn.close()
                return False
            else :
                pw = getpass.getpass('비밀번호 : ')

        cur.execute('SELECT * FROM users WHERE id = ? ', (id, ))

        if cur.fetchone():
            print('이미 존재하는 아이디입니다.')
            if input('취소하시겠습니까?(Y/N) ') == 'Y':
                conn.close()
                return False              
        else:
            cur.execute('INSERT INTO users VALUES (?, ?, ?)', (id, pw, ''))
            conn.commit()
            conn.close()
            return True
