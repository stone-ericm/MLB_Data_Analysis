# import requests
# from bs4 import BeautifulSoup
# from requests_html import HTMLSession
from models import *
import sqlalchemy as alchemy
from sqlalchemy import MetaData, insert, create_engine, Table
from sqlalchemy.orm import load_only
from models import Records, Franchises
from statistics import mean

engine = create_engine("postgresql://postgres:password@localhost/MLB_app")
# engine.echo = True
Session = alchemy.orm.sessionmaker(bind=engine)
alc_session = Session()
records = alc_session.query(Records)
franchises = alc_session.query(Franchises)


def grab_team_all_records(team):
    return records.filter(Records.team_id).all()


def grab_team_by_year(team, year):
    return records.filter(Records.team_id == team, Records.year == year).all()


def average_record_by_team(team):
    annual_records = records.filter(Records.team_id == team).all()
    collective_win_percentages = []
    # print(annual_records)
    for each in annual_records:
        win_percent = each.wins / (each.losses + each.wins)
        collective_win_percentages.append(win_percent)
    average_season = mean(collective_win_percentages)
    return("The average win percentage for {} is {:.3f}".format(team, average_season))


def years_until_500_season():
    expansion_franchises = franchises.filter(
        Franchises.expansion == True).options(load_only("team_id")).all()
    fivehundred_plus_year = []
    for team in expansion_franchises:
        annual_records_exp_teams = records.filter(
            Records.team_id == team.team_id).all()
        for year in annual_records_exp_teams:
            win_percent = year.wins / (year.losses + year.wins)
            if win_percent >= .500:

                fivehundred_plus_year.append(year.year - team.org_founded)
                break
    return(fivehundred_plus_year)


def years_until_consecutive_500_seasons():
    expansion_franchises = franchises.filter(
        Franchises.expansion == True).options(load_only("team_id")).all()
    fivehundred_plus_year = {}
    for team in expansion_franchises:
        annual_records_exp_teams = records.filter(
            Records.team_id == team.team_id).all()
        flag = False
        for year in annual_records_exp_teams:
            win_percent = year.wins / (year.losses + year.wins)
            if win_percent >= .500:
                if flag == True:
                    fivehundred_plus_year[team.team_id] = (
                        year.year - team.org_founded)
                    break
                else:
                    flag = True
            else:
                flag = False
    return(fivehundred_plus_year)


def average_expansion_and_non_record():
    annual_records = records.join(Franchises).all()

    # print(annual_records[0].franchise.expansion)
    # quit()
    collective_win_percentages_exp = []
    collective_win_percentages_non_exp = []
    # print(annual_records)
    for each in annual_records:
        if each.year >= 1961:
            win_percent = each.wins / (each.losses + each.wins)
            if each.franchise.expansion == True:
                collective_win_percentages_exp.append(win_percent)
            else:
                collective_win_percentages_non_exp.append(win_percent)
    average_season_exp = mean(collective_win_percentages_exp)
    average_season_non_exp = mean(collective_win_percentages_non_exp)
    return("The average win percentage for a non-expansion team since 1961 is {:.3f}.\nThe average win percentage for an expansion team is {:.3f}.".format(average_season_non_exp, average_season_exp))


def annual_expansion_and_non_record():
    for year in range(1961, 2020):
        collective_win_percentages_exp = []
        collective_win_percentages_non_exp = []
        team_records = records.join(Franchises).filter(
            Records.year == year).all()
        for each in team_records:
            win_percent = each.wins / (each.losses + each.wins)
            if each.franchise.expansion == True:
                collective_win_percentages_exp.append(win_percent)
            else:
                collective_win_percentages_non_exp.append(win_percent)
        row = Annual_Expansion_And_Non_Record(
            year=year,
            non_exp=mean(collective_win_percentages_non_exp),
            exp=mean(collective_win_percentages_exp)
        )
        session.add(row)
    session.commit()
    # print("The average win percentage for a non-expansion team in {} was {:.3f}.\nThe average win percentage for an expansion team in that year was {:.3f}.".format(
    # year, mean(collective_win_percentages_non_exp), mean(collective_win_percentages_exp)))


print(annual_expansion_and_non_record())

# Is having a worse winning percentage coorelated with being expansion?
# Do expansion teams have winning seasons at the same rate as originals?
