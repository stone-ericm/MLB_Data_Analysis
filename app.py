# import requests
# from bs4 import BeautifulSoup
# from requests_html import HTMLSession
import sqlalchemy as alchemy
from sqlalchemy import MetaData, insert, create_engine, Table
from models import Records, Franchises
from statistics import mean

engine = create_engine("sqlite:///app.db")
# engine.echo = True
Session = alchemy.orm.sessionmaker(bind=engine)
alc_session = Session()

'''
Lets figure out the average season for each team
and again maybe with some number of early years excluded as a buffer
for expansion teams

What's the average number of years before an expansion team has a .500+ record?
'''
team_ids = []
team_records = {}
franchise_objects = alc_session.query(Franchises).all()
for each in franchise_objects:
    team_ids.append(each.team_id)
for team in team_ids:
    print(team)
    team_records[team] = alc_session.query(
        Records).filter_by(team_id=team).all()
# team_records in each loop contains the records for one respective team as an instance of Records
    # years_in_operation = len(team_records)
    # print(years_in_operation)
len(team_records)
print(team_records)
collective_win_percentages = []
for i, each in team_records:
    for each in each:
        win_percent = each.wins / (each.losses + each.wins)
    # print(win_percent)
    collective_win_percentages.append(win_percent)
average_season = mean(collective_win_percentages)
print("The average win percentage for {} is {:.3f}".format(team, average_season))

# session = HTMLSession()
# year = str(2020)
# URL = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=br&url=%2Fleagues%2FMLB%2F" + year + \
#     "-standings.shtml&div=div_expanded_standings_overall&del_col=1,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30"
# r = session.get(URL)
# print(r)

# soup = BeautifulSoup(r.content, 'html.parser')

# table = soup.find(id="expanded_standings_overall")

# # print(table.findAll("tr")[0])
# # print(table.findAll("tr")[1]("td")[0].get_text())

# # record_instance = Records(
# #     year=int(year)
# #     team=)

# f = open("modern_names", "w")


# counter = 0
# # while counter < 2:
# for row in table.findAll("tr"):
#     # for cell in row("td"):
#     #     print(cell.get_text())
#     if row("td") != [] and row("td")[0].get_text() != "Avg":
#         f.write(row("td")[0].get_text() + "\n")
# print(row("td"))
# new_record = Records(
#     year=int(year),
#     team=row("td")[0].get_text(),
#     league=row("td")[1].get_text(),
#     wins=row("td")[2].get_text(),
#     losses=row("td")[3].get_text()
# )
# print(new_record.year)
# print(new_record.team)
# print(new_record.league)
# print(new_record.wins)
# print(new_record.losses)
# print(new_record.org_founded)
# break


# print(row("td"))
# break
# for cell in row("td"):
# print(cell.get_text().strip())


# f.close()

# 2020_record = results.find_all('section', class_='')
# print(results.prettify())
