from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, DateField, IntegerField
from wtforms.validators import DataRequired, Optional


class NewEntries(FlaskForm):
    title = StringField(
        'title',
        validators=[DataRequired()]
    )
    date = DateField(
        'Date in YYY-M-D format',
        validators=[DataRequired()],
        format='%Y-%m-%d'
    )
    time_spent = IntegerField(
        'Time Spent rounded to nearest hour',
        validators=[DataRequired()]
    )
    learned = TextAreaField(
        'things i learned',
        validators=[DataRequired()]
    )
    resourses = TextAreaField(
        'Handy resourses',
        validators=[Optional()]
    )
