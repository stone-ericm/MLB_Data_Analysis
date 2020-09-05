from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv
from models import *
engine = create_engine("sqlite:///app.db")
# engine.echo = True
Session = alchemy.orm.sessionmaker(bind=engine)
session = Session()
html_session = HTMLSession()

URL = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=br&url=%2Fleagues%2FMLB%2F{}-standings.shtml&div=div_expanded_standings_overall&del_col=1,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30"


alt_names = {}
an = open("alt_names", "r")
reader = csv.reader(an)
for line in reader:
    if line[1] not in alt_names:
        alt_names[line[0].strip()] = line[1].strip()
    # else:
    #     alt_names[line[1]].append(line[0])
an.close()

additional_info = {}
ai = open("team_additional_info", "r")
reader = csv.reader(ai)
for line in reader:
    additional_info[line[0].strip()] = [int(line[1]), bool(int(line[2]))]
ai.close()

modern_names = []
mn = open("modern_names", "r")
for line in mn:
    modern_names.append(line.strip())

'''

requested info comes in the following order:
PIT, NL, WINS, LOSSES


'''

for year in range(1901, 2020):
    # URL = URL_1 + str(year) + URL_2
    r = html_session.get(URL.format(str(year)))
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find(id='expanded_standings_overall')
    for row in table.findAll("tr"):
        if row("td") != [] and row("td")[0].get_text() != "Avg":
            if row("td")[1].get_text() in ["NL", "AL"]:
                team_id = row("td")[0].get_text()
                if team_id in alt_names:
                    team_id = alt_names[team_id]
                league = row("td")[1].get_text()
                wins = row("td")[2].get_text()
                losses = row("td")[3].get_text()
                new_record = Records(
                    year=year,
                    team_id=team_id,
                    league=league,
                    wins=wins,
                    losses=losses,
                    org_founded=additional_info[team_id][0],
                    expansion=additional_info[team_id][1]
                )
                session.add(new_record)
    print(year)

for team_id in modern_names:
    new_team = Franchises(
        team_id=team_id
    )
    session.add(new_team)

session.commit()
