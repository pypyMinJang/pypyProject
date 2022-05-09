import requests
import sqlite3
import re
from bs4 import BeautifulSoup as bs

def scheduel_crawling(url, selecPath, db_uri, file_uri):
    page = requests.get(url)
    soup = bs(page.text, "html.parser")

    elements = soup.select(selecPath)

    conn = sqlite3.connect(db_uri)

    cur= conn.cursor()

    conn.execute("CREATE TABLE if not exists schedule_data(\
        date TEXT, homeTeam TEXT, score TEXT, awayTeam TEXT, stadium TEXT)")

    lst = []
    inlst = []
    for i, element in enumerate(elements, start=1):
        if element.text:
            if '(' in element.text:
                day = element.text.strip()
            else:
                if re.match("..:..", element.text):
                    inlst.append(day+' '+element.text.strip())
                elif re.findall('[ㄱ-힣]+', element.text):
                    m = re.findall('[ㄱ-힣]+', element.text)
                    st = re.sub('[ㄱ-힣]+', "", element.text).strip()
                    inlst.append(m[0])
                    inlst.append(st)
                    inlst.append(m[1])
                else:
                    inlst.append(element.text)
                    lst.append(tuple(inlst))
                    inlst = []

    cur.executemany(
        'INSERT INTO schedule_data VALUES (?, ?, ?, ?, ?)',
        lst
    )

    cur.execute("SELECT * FROM schedule_data")

    rows = cur.fetchall()
    # for row in rows:
    #     print(row)

    f = open(file_uri, 'w', encoding="UTF-8")
    for row in rows:
        for d in row:
            f.write(d+' ')
        f.write('\n')

    f.close()

