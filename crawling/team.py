import requests
import sqlite3
from bs4 import BeautifulSoup as bs

def team_crawling(url, selecPath, db_uri, file_uri):
    page = requests.get(url)
    soup = bs(page.text, "html.parser")

    elements = soup.select(selecPath)

    conn = sqlite3.connect(db_uri)

    cur= conn.cursor()

    conn.execute("CREATE TABLE if not exists team_data(teamName TEXT, match INTEGER, winScore INTEGER, \
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

    cur.executemany(
        'INSERT INTO team_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        lst
    )

    cur.execute("SELECT * FROM team_data")

    rows = cur.fetchall()
    # for row in rows:
    #     print(row)


    f = open(file_uri, 'w', encoding="UTF-8")
    for row in rows:
        for d in row:
            f.write(str(d)+' ')
        f.write('\n')

    f.close()
