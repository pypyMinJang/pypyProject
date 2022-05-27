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

signed = input('회원 가입 하셨습니까?(Y/N) ')
while True:
    if signed == 'Y' :
        id = input('아이디 : ')
        pw = getpass.getpass('비밀번호 : ')
        user = login.login(id, pw)
        break
    elif signed == 'N' :
        if login.signing():
            print("회원 가입")
            id = input('아이디 : ')
            pw = getpass.getpass('비밀번호 : ')
            user = login.login(id, pw)
            break
    else :
        print('(Y/N)으로 답변해주십시오.')
    signed = input('회원 가입 하셨습니까?(Y/N)')

print("환영합니다~!!")
print()
print("메뉴 선택창")

while True:
    print("""
1. EPL 일정\t\t2. 관심 팀 일정\t\t3. EPL 팀 목록
4. EPL 순위 통계\t5. 관심 팀 목록\t\t6. 관심 팀 점수 통계
7. 관심 팀 추가\t\t8. 관심 팀 삭제\t\t9. 비밀번호 변경
10. 계정 삭제\t\t11. 앱 종료
     """)
    print("'{}'님의 메뉴 선택 : ".format(user.id), end='')
    commd = input()

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
            print("Bye..")
            break
    elif commd == '11' or commd == "앱 종료":
        user.logout()
        print("앱이 종료되었습니다.")
        print()
        break
    else :
        recommd = input("앱을 종료하시겠습니까??(Y/N) ")
        while(True):
            if recommd == 'Y':
                print("앱이 종료되었습니다.")
                print()
                break
            elif recommd == 'N':
                print("다시 시작하겠습니다.")
                print()
                break
            else :
                print("(Y/N)으로 답변해주십시오.")
                print()
                
            recommd = input("앱을 종료하시겠습니까??(Y/N) ")
            
        if(recommd=='Y'):
            break


