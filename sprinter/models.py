from sprinter.connectdatabase import ConnectDatabase
from peewee import *


class Entries(Model):
    title = CharField()
    text = CharField()
    acc_crit = CharField()
    bus_value = IntegerField()
    estimation = IntegerField()
    status = CharField()

    class Meta:
        database = ConnectDatabase.db
