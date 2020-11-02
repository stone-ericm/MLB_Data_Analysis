from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv
from models import *
from statistics import mean
from datetime import datetime


def populate_database():
    engine = create_engine("postgresql://postgres:password@localhost/MLB_app")
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

    for team_id in modern_names:
        new_team = Franchises(
            team_id=team_id,
            org_founded=additional_info[team_id][0],
            expansion=additional_info[team_id][1]
        )
        session.add(new_team)

    session.commit()

    '''

    requested info comes in the following order:
    PIT, NL, WINS, LOSSES


    '''

    for year in range(1901, 2021):
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
                        year=datetime.strptime(str(year), '%Y'),
                        team_id=team_id,
                        league=league,
                        wins=wins,
                        losses=losses,
                        franchise=(session.query(Franchises).filter(
                            Franchises.team_id == team_id).first())
                    )

                    session.add(new_record)
        print(year)

    session.commit()

    for year in range(1961, 2021):
        records = session.query(Records)
        collective_win_percentages_exp = []
        collective_win_percentages_non_exp = []
        team_records = records.join(Franchises).filter(
            Records.year == datetime.strptime(str(year), '%Y')).all()
        for each in team_records:
            win_percent = each.wins / (each.losses + each.wins)
            if each.franchise.expansion == True:
                collective_win_percentages_exp.append(win_percent)
            else:
                collective_win_percentages_non_exp.append(win_percent)
        # print(collective_win_percentages_exp)
        # print(collective_win_percentages_non_exp)
        row = Annual_Expansion_And_Non_Record(
            year=datetime.strptime(str(year), '%Y'),
            non_exp=mean(collective_win_percentages_non_exp),
            exp=mean(collective_win_percentages_exp)
        )
        session.add(row)
    session.commit()

    for team in modern_names:
        records = session.query(Records)
        annual_records = records.filter(Records.team_id == team).all()
        collective_win_percentages = []
        # print(annual_records)
        for each in annual_records:
            win_percent = each.wins / (each.losses + each.wins)
            collective_win_percentages.append(win_percent)
        average_season = mean(collective_win_percentages)
        row = Average_Record_By_Team(
            team_id=team,
            win_pct=average_season
        )
        session.add(row)
    session.commit()

    ws_winners = {}
    ws = open("WS_winners", "r")
    reader = csv.reader(ws)
    for line in reader:
        ws_winners[int(line[0])] = line[1].strip()
    ws.close()

    for year in list(ws_winners.keys()):
        row = World_Series_Winners(
            year=datetime.strptime(str(year), '%Y'),
            winner=ws_winners[year]
        )
        session.add(row)
    session.commit()

    elo_csv = open("mlb_elo.csv", "r")
    reader = csv.reader(elo_csv)
    next(reader)
    for line in reader:
        row = ELO(
            date=datetime.strptime(str(line[0]), '%Y-%m-%d'),
            team=line[4],
            elo=line[10]
        )
        session.add(row)
        row = ELO(
            date=datetime.strptime(str(line[0]), '%Y-%m-%d'),
            team=line[5],
            elo=line[11]
        )
        session.add(row)
    session.commit()


if __name__ == "__main__":
    populate_database()
