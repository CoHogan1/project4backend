from peewee import *
import datetime
from flask_login import UserMixin
# heroku deployment additions
import os
from playhouse.db_url import connect


#DATABASE = SqliteDatabase('users.sqlite') # non heroku

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///users.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True) # all askey chars.
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


def init():
    print("Initializing database")
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
