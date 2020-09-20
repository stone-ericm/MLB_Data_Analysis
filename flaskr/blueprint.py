from flask import (Blueprint, flash, redirect,
                   render_template, request, url_for)
from werkzeug.exceptions import abort
from models import *
import sqlalchemy as alchemy
from sqlalchemy import MetaData, insert, create_engine, Table

engine = create_engine("postgresql://postgres:password@localhost/MLB_app")
Session = alchemy.orm.sessionmaker(bind=engine)
alc_session = Session()
# records = alc_session.query(Records)
franchises = alc_session.query(Franchises)


bp = Blueprint('blueprint', __name__)

teams = [r[0] for r in alc_session.query(
    Average_Record_By_Team.team_id)]
print(teams)


@bp.route('/team_avg_db', methods=('GET', 'POST'))
def team_avg_db():
    if request.method == 'POST':
        avg_record = {}
        team_id = request.form['team_id']
        error = None

        avg_record[team_id] = round(alc_session.query(Average_Record_By_Team).filter(
            Average_Record_By_Team.team_id == team_id).all()[0].win_pct, 3)
        return render_template('team_avg.html', teams=teams, team_avg=avg_record)
    else:
        return render_template('team_avg.html', teams=teams, team_avg=None)
