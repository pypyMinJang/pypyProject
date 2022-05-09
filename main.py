import sys
from crawling.team import team_crawling
from crawling.schedule import scheduel_crawling

url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=EPL"
db_uri = "./data/data.db"

selecPath = '#teamRankTabPanel_0 > div > div.scroll > table > tbody > tr > td'
file_uri = "./data/team.txt"
team_crawling(url, selecPath, db_uri, file_uri)

selecPath = '#myschedule > table > tbody > tr > td'
file_uri = "./data/schedule.txt"
scheduel_crawling(url, selecPath, db_uri, file_uri)

print("hello world!")