import sqlite3
import unicodedata

import getpass

from . import CONSTANT as const

def fill_str_with_space(input_s="", max_size=40, fill_char=" ", side='left'):
    """
    - 길이가 긴 문자는 2칸으로 체크하고, 짧으면 1칸으로 체크함. 
    - 최대 길이(max_size)는 40이며, input_s의 실제 길이가 이보다 짧으면 
    남은 문자를 fill_char로 채운다.
    """
    l = 0 
    for c in input_s:
        if unicodedata.east_asian_width(c) in ['F', 'W']:
            l+=2
        else: 
            l+=1
   
    if side == 'right':
        return fill_char*(max_size-l)+input_s
    elif side == 'center':
        return fill_char*((max_size-l)//2)+input_s+fill_char*((max_size-l)//2)
    else:
        return input_s+fill_char*(max_size-l)
def printScoreMenu():
    print(fill_str_with_space("팀명",13),end='')
    print(fill_str_with_space("경기수",8),end='')
    print(fill_str_with_space("승점",8),end='')
    print(fill_str_with_space("승",8),end='')
    print(fill_str_with_space("무",8),end='')
    print(fill_str_with_space("패",8),end='')
    print(fill_str_with_space("득점",8),end='')
    print(fill_str_with_space("실점",8),end='')
    print(fill_str_with_space("득실차",8))
def printScheduleMenu():
    print(fill_str_with_space("일시",17),end='')
    print(fill_str_with_space("홈팀",14, ' ', 'right'),end='')
    print(fill_str_with_space("결과 ",7, ' ', 'center'),end='')
    print(fill_str_with_space("어웨이팀",14),end='')
    print(fill_str_with_space("스타디움",30))

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

        conn.close()
        return

    def seeAllSchedule(self):
        conn = sqlite3.connect(const._DB_URI)
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM schedule")
        printScheduleMenu()
        for row in rows:
            for i, d in enumerate(row):
                if i == 1:
                    print(fill_str_with_space(d, 13, ' ', 'right'), end=' ')
                elif i == 3:
                    print(fill_str_with_space(d, 13), end=' ')
                else:
                    print(d, end=' ')

            print("")

        conn.close()
        return
    def seeCheckedSchedule(self):
        if self.id != 'guest':
            if self.checked:
                conn = sqlite3.connect(const._DB_URI)
                cur = conn.cursor()
                cur.execute("SELECT * FROM schedule")
                printScheduleMenu()
                while True:
                    row = cur.fetchone()
                    if row == None:
                        break
                    if row[1] in self.checked or row[3] in self.checked:
                        for i, d in enumerate(row):
                            if i == 1:
                                print(fill_str_with_space(d, 13, ' ', 'right'), end=' ')
                            elif i == 3:
                                print(fill_str_with_space(d, 13), end=' ')
                            else:
                                print(d, end=' ')
                        print("")
                
                conn.close()
            else:
                print("관심 팀을 먼저 등록해 주세요")
        else:
            print("guest로는 이용할수 없습니다")
        return
    def seeAllTeam(self):
        conn = sqlite3.connect(const._DB_URI)
        cur = conn.cursor()
        cur.execute("SELECT * FROM team")
        rows = cur.fetchall()
        for i, row in enumerate(rows, start=1):
            print(fill_str_with_space(row[0], 13), end='')
            if i % 5 == 0:
                print()

        conn.close()

        return
       
    def seeAllTeam_Score(self):
        conn = sqlite3.connect(const._DB_URI)
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM team")
        printScoreMenu()
        for row in rows:
            for i, d in enumerate(row):
                if i == 0:
                    print(fill_str_with_space(d,13), end='')
                else :
                    print('{:<8}'.format(d), end='')
            print("")

        conn.close()
        return
    def seeCheckedTeam(self):
        if self.id != 'guest':
            if self.checked:
                for team in self.checked:
                    print(team, end=' ')
                print('')
            else:
                print('관심 팀을 먼저 등록해 주세요')
        else:
            print("guest로는 이용할수 없습니다")
        return 
    def seeCheckedTeam_Score(self):
        if self.id != 'guest':
            if self.checked:
                conn = sqlite3.connect(const._DB_URI)
                cur = conn.cursor()
                printScoreMenu()
                cur.execute("SELECT * FROM team")
                while True:
                    row = cur.fetchone()
                    if row == None:
                        break
                    if row[0] in self.checked:
                        for i, d in enumerate(row):
                            if i == 0:
                                print(fill_str_with_space(d,13), end='')
                            else :
                                print('{:<8}'.format(d), end='')
                        print("")

                conn.close()
            else:
                print('관심 팀을 먼저 등록해 주세요')
        else:
            print('guest로는 이용할수 없습니다')
        return

    def addCheckedTeam(self):
        if self.id != 'guest':
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

            cur.execute("UPDATE users SET checked = ? WHERE id = ?", (' '.join(self.checked), self.id))
            conn.commit()
            conn.close()
        else:
            print('guest로는 이용할수 없습니다')
        return
    def deleteCheckedTeam(self):
        if self.id != 'guest':
            if self.checked:
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
                
                conn = sqlite3.connect(const._DB_URI)
                cur = conn.cursor()
                cur.execute("UPDATE users SET checked = ? WHERE id = ?", (' '.join(self.checked), self.id))
                conn.commit()
                conn.close()
            else:
                print("관심 팀을 먼저 등록해 주세요")
        else:
            print('guest로는 이용할수 없습니다')
        return

    def resetPW(self):
        if self.id != 'guest':
            if self.pw == getpass.getpass('현재 비밀번호 : '):
                pw = getpass.getpass('새 비밀번호 : ')
                while pw == '' or ' ' in pw or '\t' in pw:
                    print('공백 없는 비밀번호를 부탁드립니다..')
                    if input('취소하시겠습니까?(Y/N) ') == 'Y':
                        return
                    else :
                        pw = getpass.getpass('새 비밀번호 : ')

                self.pw = pw
            else:
                print('비밀번호가 틀립니다')
        else:
            print('guest로는 이용할수 없습니다')
        return
    def deleteID(self):
        if self.id != 'guest':
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
                    conn.close()
                    return True
                else :
                    print("틀린 비밀번호 :)")
                conn.close()
            else :
                print("좋은 시간 보내십시오.")        
        else:
            print('guest로는 이용할수 없습니다')

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
    
        

