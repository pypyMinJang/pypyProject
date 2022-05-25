import sqlite3
import getpass
import datetime

from crawling.team import team_crawling
from crawling.schedule import scheduel_crawling
import user.login as login
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
        if login.signing():
            print("login now!")
            id = input('id : ')
            pw = getpass.getpass('pw : ')
            user = login.login(id, pw)
            break
    else :
        print('?')

print("welcome~")

while True:
    print("""
1. seeAllSchedule\t2. seeCheckedSchedule\t3. seeAllTeam
4. seeAllTeam_Score\t5. seeCheckedTeam\t6. seeCheckedTeam_Score
7. addCheckedTeam\t8. deleteCheckedTeam\t9. resetPW
10. deleteID\t11. exit
     """)
    print("What's you want {} ? ".format(user.id), end='')
    commd = input()

    if commd == '1' or commd == "seeAllSchedule":
        user.seeAllSchedule()
    elif commd == '2' or commd == "seeCheckedSchedule":
        user.seeCheckedSchedule()
    elif commd == '3' or commd == "seeAllTeam":
        user.seeAllTeam()
    elif commd == '4' or commd == "seeAllTeam_Score":
        user.seeAllTeam_Score()
    elif commd == '5' or commd == "seeCheckedTeam":
        user.seeCheckedTeam()
    elif commd == '6' or commd == "seeCheckedTeam_Score":
        user.seeCheckedTeam_Score()
    elif commd == '7' or commd == "addCheckedTeam":
        user.addCheckedTeam()
    elif commd=='8' or  commd=="deleteCheckedTeam":
        user.deleteCheckedTeam()
    elif commd == '9' or commd == "resetPW":
        user.resetPW()
    elif commd == '10' or commd == "deleteID":
        if user.deleteID():
            print("bye..")
            break
    elif commd == '11' or commd == "exit":
        user.logout()
        print("bye~")
        break
    else :
        recommd = input("do you want exit?(Y/N) ")
        if recommd == 'Y':
            print("bye~")
            break
        elif recommd == 'N':
            print("ok")
        else :
            print("I can't understand what are you saying..")

