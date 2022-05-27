import sqlite3
import getpass

from . import CONSTANT as const

class User:
    id = 'guest'
    pw = 'guest'
    checked = []

    def __init__(self, id, pw):
        conn = sqlite3.connect(const._DB_URI)
        cur = conn.cursor()
    

        conn.execute("CREATE TABLE if not exists users(\
        id TEXT, pw TEXT, checked TEXT)")
        cur.execute('SELECT * FROM users WHERE id = ? AND pw = ?', (id, pw))

        if cur.fetchone() :
            self.id = id
            self.pw = pw
            cur.execute('SELECT * FROM users WHERE id = ? AND pw = ?', (id, pw))
            self.checked = str(cur.fetchone()[2]).split(' ')
            if '' in self.checked:
                self.checked.remove('')
        else :
            print("로그인 실패. 'guest'로 로그인 합니다.")

    def seeAllSchedule(self):
        conn = sqlite3.connect(const._DB_URI)
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM schedule")
        for row in rows:
            for d in row:
                print(d, end=' ')
            print("")

        conn.close()
        return
    def seeCheckedSchedule(self):
        return
    def seeAllTeam(self):
        print("""
맨시티\t\t리버풀\t\t첼시\t\t토트넘\t\t아스날
맨유\t\t웨스트햄\t레스터\t\t브라이튼\t울버햄튼
뉴캐슬\t\t팰리스\t\t브렌트포드\t아스톤빌라\t사우스햄튼
에버턴\t\t리즈\t\t번리\t\t왓포드\t\t노리치
        """)
        
    def seeAllTeam_Score(self):
        conn = sqlite3.connect(const._DB_URI)
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM team")
        for row in rows:
            for i, d in enumerate(row):
                if i == 0:
                    print('{:<8}'.format(d), end='')
                else :
                    print(d, end=' ')
            print("")

        conn.close()
        return
    def seeCheckedTeam(self):
        for team in self.checked:
            print(team, end=' ')
        print('')
        return 
    def seeCheckedTeam_Score(self):
        return

    def addCheckedTeam(self):
        conn = sqlite3.connect(const._DB_URI)
        cur = conn.cursor()

        while True:
            teamName = input("추가할 팀 : ")
            cur.execute("SELECT * FROM team WHERE teamName = ?", (teamName, ))
            if cur.fetchone():
                self.checked.append(teamName)
                if input("다른 팀도 추가하시겠습니까?(Y/N) ") != 'Y':
                    break
            else:
                print("그런 팀은 없습니다.")
                if input("메뉴 선택 창으로 돌아가시겠습니까?(Y/N) ") == 'Y':
                    break

        return
    def deleteCheckedTeam(self):
        while True:
            teamName = input("삭제할 팀 : ")
            if teamName in self.checked:
                self.checked.remove(teamName)
                if input("다른 팀도 삭제하시겠습니까?(Y/N) ") != 'Y':
                    break
            else:
                print("그런 팀은 없습니다.")
                if input("메뉴 선택 창으로 돌아가시겠습니까?(Y/N) ") == 'Y':
                    break

        return

    def resetPW(self):
        pw = getpass.getpass('새 비밀번호 : ')
        while pw == '' or ' ' in pw or '\t' in pw:
            print('공백 없는 비밀번호를 부탁드립니다..')
            if input('취소하시겠습니까?(Y/N) ') == 'Y':
                return
            else :
                pw = getpass.getpass('새 비밀번호 : ')

        self.pw = pw
        return
    def deleteID(self):
        assertion = input("정말로 삭제하시겠습니까?(Y/N) : ")
        if assertion == 'Y':
            conn = sqlite3.connect(const._DB_URI)
            cur = conn.cursor()
            pw_comfirm = input("비밀번호 : ")
            cur.execute('SELECT * FROM users WHERE id = ? AND pw = ?', (self.id, pw_comfirm))
            if cur.fetchone():
                print("안녕히 가십시오..")
                cur.execute('DELETE FROM users WHERE id = ?', (self.id, ))
                conn.commit()
                return True
            else :
                print("틀린 비밀번호 :)")
            conn.close()
        else :
            print("좋은 시간 보내십시오.")        

        return False

    def logout(self):
        if self.id != 'guest':
            conn = sqlite3.connect(const._DB_URI)
            cur = conn.cursor()
            cur.execute("UPDATE users SET pw = ? WHERE id = ?", (self.pw, self.id))
            cur.execute("UPDATE users SET checked = ? WHERE id = ?", (' '.join(self.checked), self.id))

            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            f = open(const._USERS_FILE_URI, 'w', encoding="UTF-8")
            for row in rows:
                for d in row:
                    f.write(d+' ')
                f.write('\n')

            f.close()

            conn.commit()
            conn.close()
        return
    
        

