"""manage.py
CLI Usage:
---------
    $ python manage.py [command] [param] [param] ...
Help
    $ python manage.py help
Recreate the database
    $ python manage.py recreate_db
Available commands are:
    help            Show this help
    recreate_db     Recreate the database
"""

from flask.cli import FlaskGroup

from app import create_app, db


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("help")
def help():
    print(__doc__)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()