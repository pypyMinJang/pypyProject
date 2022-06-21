import sqlite3
import datetime
import time
import getpass

import preprocess as pre

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

from crawling.team import team_crawling
from crawling.schedule import scheduel_crawling
from user.user import fill_str_with_space
import user.login as login
import CONSTANT as const

def enter():
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

    return user
def printMenu(menus):
    print("\n메뉴[ 원하는 메뉴의 번호나 이름을 입력해 주세요 ]")
    for i, menu in enumerate(menus, start=1):
        print(fill_str_with_space(menu, 20), end='')
        if i%3 == 0:
            print()
    print()

pre.createDirectory(const._DB_FOLDER_URI)

conn = sqlite3.connect(const._DB_URI)
cur = conn.cursor()
now = datetime.datetime.now()

conn.execute("CREATE TABLE if not exists updated( \
        type TEXT, date TEXT)")

cur.execute('SELECT date FROM updated WHERE type = ?', ('team', ))
if cur.fetchone():
    cur.execute('SELECT date FROM updated WHERE type = ?', ('team', ))
    lated = datetime.datetime.strptime(cur.fetchone()[0], '%Y-%m-%d %H:%M:%S.%f')
    if (now-lated).days >= 1:
        print("점수 정보 가져오는 중...")
        team_crawling()
        print("점수 정보 가져오기 성공!")
else:
    print("점수 정보 가져오는 중...")
    team_crawling()
    print("점수 정보 가져오기 성공!")


cur.execute('SELECT date FROM updated WHERE type = ?', ('schedule', ))
if cur.fetchone():
    cur.execute('SELECT date FROM updated WHERE type = ?', ('schedule', ))
    lated = datetime.datetime.strptime(cur.fetchone()[0], '%Y-%m-%d %H:%M:%S.%f')
    if (now-lated).days >= 1:
        print("경기일정 가져오는 중...")
        scheduel_crawling()
        print("경기일정 가져오기 성공!")
else:
    print("경기일정 가져오는 중...")
    scheduel_crawling()
    print("경기일정 가져오기 성공!")

conn.close()

user = enter()

print("환영합니다~!!\n")

menus = [\
    "1. EPL 일정", "2. 관심 팀 일정", "3. EPL 팀 목록", \
    "4. EPL 순위 통계", "5. 관심 팀 목록", "6. 관심 팀 점수 통계", \
    "7. 관심 팀 추가", "8. 관심 팀 삭제", "9. 비밀번호 변경", \
    "10. 계정 변경", "11. 계정 삭제", "12. 프로그램 종료"]
while True:
    time.sleep(0.5)
    printMenu(menus)
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

    elif commd == '10' or commd == "계정 변경":
        user.logout()
        user = enter()

    elif commd == '11' or commd == "계정 삭제":
        if user.deleteID():
            break

    elif commd == '12' or commd == "프로그램 종료":
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