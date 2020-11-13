import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')


class JournalEntries(Model):
    id = AutoField()
    title = CharField(max_length=200)
    time_spent = IntegerField()
    learned = TextField()
    resourses = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def add_entries(cls, title, time_spent, learned, resourses, date):
        try:
            with DATABASE.transaction():
                cls.create(
                    title=title,
                    time_spent=time_spent,
                    learned=learned,
                    resourses=resourses,
                    date=date,
                )
        except IntegrityError:
            raise ValueError('Something went wrong')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([JournalEntries], safe=True)
    DATABASE.close()
