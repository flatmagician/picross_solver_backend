from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class GridSelectForm(FlaskForm):
    rows = StringField('Rows')
    cols = StringField('Cols')
    submit = SubmitField('Sign In')
