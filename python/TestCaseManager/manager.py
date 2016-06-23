#!/usr/bin/python

from flask.ext.script import Server, Manager
from app.models import User, Case, Result

from app import app
from app import db


manager = Manager(app, usage="Perform database operations")

def prompt_bool(prompt):

    answer=raw_input(prompt)
    if str(answer) == "YES":
        return True
    else:
        return False

@manager.command
def drop():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data:"):
        db.drop_all()
        print "Sucessfully drop database"

@manager.command
def add_user(username, password, email):
    user = User(username=username, password=password, email=email)
    user.save()
    print "Add user:%s success" %username
    return user


@manager.command
def list_user(username):

    user = User.query.filter(username==User.username).first_or_404()
    if user:
        print "User Info:"
        print "  id     : %s"%user.id
        print "  name   : %s"%user.username
        print "  email  : %s"%user.email

    else:
        print "No such user:%s"%username


@manager.command
def create(default_data=True, sample_data=False):
    "Creates database tables from sqlalchemy models"
    db.create_all()

    ray = add_user(username="ray", password="ray", email="ray.chen@emc.com")
    simon = add_user(username="simon", password="simon", email="Simon.Yang@emc.com")
    xiang = add_user(username="xiang", password="xiang", email="Xiang.Zhang2@emc.com")

    case = Case(name="TestCase001", author_id=ray.id,
        description = "This is the first test case"
    )
    case.save()

    result = Result(name="TestResult001" , author_id=ray.id,
        link="http://www.baidu.com", case_id=case.id
    )
    result.save()


    #populate(default_data, sample_data)


@manager.command
def recreate(default_data=True, sample_data=False):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()
    create(default_data, sample_data)


@manager.command
def populate(default_data=False, sample_data=False):
    "Populate database with default data"
    from fixtures import dbfixture

    if default_data:
        from fixtures.default_data import all
        default_data = dbfixture.data(*all)
        default_data.setup()

    if sample_data:
        from fixtures.sample_data import all
        sample_data = dbfixture.data(*all)
        sample_data.setup()


if __name__ == "__main__":
    manager.run()
