import sqlite3
import re
import datetime

import requests
from bs4 import BeautifulSoup as bs

from . import CONSTANT as const

def scheduel_crawling():
    page = requests.get(const._URL)
    soup = bs(page.text, "html.parser")
    getTime = datetime.datetime.now()

    elements = soup.select(const._SCHEDULE_PATH)

    conn = sqlite3.connect(const._DB_URI)

    cur= conn.cursor()

    conn.execute("CREATE TABLE if not exists schedule(\
        date TEXT, homeTeam TEXT, score TEXT, awayTeam TEXT, stadium TEXT)")

    lst = []
    inlst = []
    for element in elements:
        if element.text:
            if '(' in element.text:
            # if re.match("..\...\.\ \(.\)", element.text):
                day = element.text.strip()
            else:
                if re.match("..:..", element.text):
                    inlst.append(day+' '+element.text.strip())
                elif re.findall('[ㄱ-힣]+', element.text):
                    m = re.findall('[ㄱ-힣]+', element.text)
                    st = re.sub('[ㄱ-힣]+', "", element.text).strip()
                    inlst.extend([m[0], st, m[1]])
                else:
                    inlst.append(element.text)
                    lst.append(tuple(inlst))
                    inlst = []
                    
    for d in lst:
        cur.execute("SELECT score FROM schedule WHERE \
            date = ? AND homeTeam = ? AND awayTeam = ? AND stadium = ?", \
                (d[0], d[1], d[3], d[4]))

        if cur.fetchone():
            cur.execute("UPDATE schedule SET score = ? \
                WHERE date = ? AND homeTeam = ? AND awayTeam = ? AND stadium = ?", \
                    (d[2], d[0], d[1], d[3], d[4]))
        else:
            cur.execute('INSERT INTO schedule VALUES (?, ?, ?, ?, ?)', d)


    f = open(const._SCHEDULE_FILE_URI, 'w', encoding="UTF-8")
    f.write(str(getTime)+'\n')
    cur.execute("SELECT * FROM schedule")
    rows = cur.fetchall()
    for row in rows:
        for d in row:
            f.write(d+' ')
        f.write('\n')

    f.close()

    conn.execute("CREATE TABLE if not exists updated( \
        type TEXT, date TEXT)")
    cur.execute('SELECT type FROM updated WHERE type = ?', ('schedule', ))
    if cur.fetchone() :
        cur.execute("UPDATE updated SET date = ? WHERE type = ?",(str(getTime),'schedule'))
    else :
        cur.execute("INSERT INTO updated VALUES (?, ?)", ('schedule', str(getTime)))

    conn.commit()
    conn.close()