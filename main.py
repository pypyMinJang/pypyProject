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
1. EPL 일정\t\t2 관심 팀 일정\t\t3. EPL 팀 목록
4. EPL 순위 통계\t5. 관심 팀 목록\t\t6. 관심 팀 점수 통계
7. 관심 팀 추가\t\t8. 관심 팀 삭제\t\t9. 비밀번호 변경
10. 계정 삭제\t\t11. 앱 종료
     """)
    print("What's you want '{}' ? ".format(user.id), end='')
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
        recommd = input("앱을 종료하시겠습니까??(Y/N) ")
        while(recommd!='Y' and recommd!='N'):
            if recommd == 'Y':
                print("bye~")
                break
            elif recommd == 'N':
                print("ok")
                break
            else :
                print("(Y/N)으로 답변해주십시오.")
                
            recommd = input("앱을 종료하시겠습니까??(Y/N) ")
            
        if(recommd=='Y'):
            break

