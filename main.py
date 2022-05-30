import sqlite3
import datetime
import time

from crawling.team import team_crawling
from crawling.schedule import scheduel_crawling
import user.login as login
import CONSTANT as const
import preprocess as pre

try:
    import getpass
except:
    pre.install('getpass')
    import getpass
try:
    import requests
except:
    pre.install('requests')
    import requests
try:
    import bs4
except:
    pre.install('bs4')
    import bs4

pre.createDirectory(const._DB_FOLDER_URI)

conn = sqlite3.connect(const._DB_URI)
cur = conn.cursor()
now = datetime.datetime.now()

conn.execute("CREATE TABLE if not exists updated( \
        type TEXT, date TEXT)")

cur.execute('SELECT * FROM updated WHERE type = ?', ('team', ))
if cur.fetchone():
    cur.execute('SELECT * FROM updated WHERE type = ?', ('team', ))
    lated = datetime.datetime.strptime(cur.fetchone()[1], '%Y-%m-%d %H:%M:%S.%f')
    if (now-lated).days >= 1:
        team_crawling()
else:
    team_crawling()


cur.execute('SELECT * FROM updated WHERE type = ?', ('schedule', ))
if cur.fetchone():
    cur.execute('SELECT * FROM updated WHERE type = ?', ('schedule', ))
    lated = datetime.datetime.strptime(cur.fetchone()[1], '%Y-%m-%d %H:%M:%S.%f')
    if (now-lated).days >= 1:
        scheduel_crawling()
else:
    scheduel_crawling()

conn.close()

signed = input('회원 가입 하셨습니까?(Y/N) ')
while True:
    if signed == 'Y' :
        id = input('아이디 : ')
        pw = getpass.getpass('비밀번호 : ')
        user = login.login(id, pw)
        break
    elif signed == 'N' :
        if login.signing():
            print("회원 가입 성공! 지금 로그인 하세요")
            id = input('아이디 : ')
            pw = getpass.getpass('비밀번호 : ')
            user = login.login(id, pw)
            break
        else :
            print('회원가입에 실패 하였습니다.')
    else :
        print('(Y/N)으로 답변해주십시오.')
    
    signed = input('회원 가입 하셨습니까?(Y/N)')

print("환영합니다~!!\n")

while True:
    print("\n메뉴[ 원하는 메뉴의 번호나 이름을 입력해 주세요 ]")
    print("""
1. EPL 일정\t\t2. 관심 팀 일정\t\t3. EPL 팀 목록
4. EPL 순위 통계\t5. 관심 팀 목록\t\t6. 관심 팀 점수 통계
7. 관심 팀 추가\t\t8. 관심 팀 삭제\t\t9. 비밀번호 변경
10. 계정 삭제\t\t11. 프로그램 종료
     """)
    commd = input("'{}'님의 메뉴 선택 : ".format(user.id))

    if commd == '1' or commd == "EPL 일정":
        user.seeAllSchedule()

    elif commd == '2' or commd == "관심 팀 일정":
        user.seeCheckedSchedule()

    elif commd == '3' or commd == "EPL 팀 목록":
        user.seeAllTeam()

    elif commd == '4' or commd == "EPL 순위 통계":
        user.seeAllTeam_Score()

    elif commd == '5' or commd == "관심 팀 목록":
        user.seeCheckedTeam()

    elif commd == '6' or commd == "관심 팀 점수 통계":
        user.seeCheckedTeam_Score()

    elif commd == '7' or commd == "관심 팀 추가":
        user.addCheckedTeam()

    elif commd=='8' or  commd=="관심 팀 삭제":
        user.deleteCheckedTeam()

    elif commd == '9' or commd == "비밀번호 변경":
        user.resetPW()

    elif commd == '10' or commd == "계정 삭제":
        if user.deleteID():
            break

    elif commd == '11' or commd == "프로그램 종료":
        user.logout()
        break

    else :
        recommd = input("프로그램을 종료하시겠습니까?(Y/N) ")
        while True :
            if recommd == 'Y':
                break
            elif recommd == 'N':
                print("다시 시작하겠습니다.\n")
                break
            else :
                print("(Y/N)으로 답변해주십시오.\n")  
                recommd = input("프로그램을 종료하시겠습니까?(Y/N) ")

        if recommd == 'Y':
            break

print("프로그램이 종료됩니다.\n")

time.sleep(1)