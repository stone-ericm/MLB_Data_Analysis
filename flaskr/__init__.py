import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # page where user can pick a team and the page will return the team's average record(by DB query)
    from . import blueprint
    app.register_blueprint(blueprint.bp)

    # @app.route('/team_avg_db')
    # def team_avg():

    # page where user can pick a team and the page will return the team's average record (though app.average_record_by_team)

    # @app.route('/team_avg_def')
    # from . import db
    # db.init_app(app)
    # from . import auth
    # app.register_blueprint(auth.bp)
    # from . import blog
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')
    return app
