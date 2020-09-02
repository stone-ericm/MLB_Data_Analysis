import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv

session = HTMLSession()

URL_1 = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=br&url=%2Fleagues%2FMLB%2F"
URL_2 = "-standings.shtml&div=div_expanded_standings_overall&del_col=1,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30"

modern_names = []
alt_names = []
mn = open("modern_names", "r")
for line in mn:
    modern_names.append(line.strip())
mn.close()

an = open("alt_names", "r+")
reader = csv.reader(an)
for line in reader:
    alt_names.append(line[0])

for year in range(1901, 2021):
    URL = URL_1 + str(year) + URL_2
    print(year)
    r = session.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find(id="expanded_standings_overall")

    for row in table.findAll("tr"):
        if row("td") != [] and row("td")[0].get_text() != "Avg":
            teamid = row("td")[0].get_text()
            if teamid not in modern_names and teamid not in alt_names and row("td")[1].get_text() in ["NL", "AL"]:
                while True:
                    action = input(teamid + "\n" + str(year) + "\n")
                    if action in modern_names:
                        an.write(teamid + ", " + action + "\n")
                        alt_names.append(teamid)
                        break
                    else:
                        pass
