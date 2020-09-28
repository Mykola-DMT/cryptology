from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class SelectKey(FlaskForm):
    key=IntegerField('Key',validators=[DataRequired()])
    submit=SubmitField('Confirm')