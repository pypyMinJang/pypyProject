import sqlite3
import datetime

import requests
from bs4 import BeautifulSoup as bs

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


    for inlst in lst:
        cur.execute("UPDATE team SET match = ? AND winScore = ? AND win = ? AND draw = ? AND lose = ?\
         AND gain = ? AND loss	= ? AND gain_loss_dif = ? WHERE teamName = ?", \
             (inlst[1], inlst[2], inlst[3], inlst[4], inlst[5], inlst[6], inlst[7], inlst[8], inlst[0]))


    f = open(const._TEAM_FILE_URI, 'w', encoding="UTF-8")
    f.write(str(getTime)+'\n')
    cur.execute("SELECT * FROM team")
    rows = cur.fetchall()
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