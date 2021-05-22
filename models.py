from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('users.sqlite')

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
