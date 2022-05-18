import requests
import sqlite3
from bs4 import BeautifulSoup as bs
import datetime

from . import CONSTANT as const

def team_crawling():
    page = requests.get(const._URL)
    soup = bs(page.text, "html.parser")
    getTime = datetime.datetime.now()

    elements = soup.select(const._TEAM_PATH)

    conn = sqlite3.connect(const._DB_URI)

    cur = conn.cursor()

    conn.execute("CREATE TABLE if not exists team(teamName TEXT, match INTEGER, winScore INTEGER, \
        win INTEGER, draw INTEGER, lose INTEGER, gain INTEGER, loss	INTEGER, gain_loss_dif INTEGER)")

    lst = []
    inlst = []
    for i, element in enumerate(elements, start=1):
        inlst.append(element.text.strip())
        if i%9 == 0:
            lst.append(tuple(inlst))
            inlst = []
    #01 02 03 04 05 06 07 08 09
    #10 11 12 13 14 15 16 17 18


    cur.execute('DELETE FROM team')
    cur.executemany(
        'INSERT INTO team VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        lst
    )

    cur.execute("SELECT * FROM team")

    rows = cur.fetchall()
    # for row in rows:
    #     print(row)

    f = open(const._TEAM_FILE_URI, 'w', encoding="UTF-8")
    f.write(str(getTime)+'\n')
    for row in rows:
        for d in row:
            f.write(str(d)+' ')
        f.write('\n')
    
    f.close()

    conn.execute("CREATE TABLE if not exists updated( \
        type TEXT, date TEXT)")
    cur.execute('SELECT * FROM updated WHERE type = ?', ('team', ))
    if cur.fetchone() :
        cur.execute("UPDATE updated SET date = ? WHERE type = ?",(str(getTime),'team'))
    else :
        cur.execute("INSERT INTO updated VALUES (?, ?)", ('team', str(getTime)))

    conn.commit()
    conn.close()