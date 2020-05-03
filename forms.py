from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired


class RenameForm(FlaskForm):
	new_name = StringField('New name', validators=[DataRequired()])
	submit = SubmitField('Rename')


class ChangePortForm(FlaskForm):
	new_port = IntegerField('New port', validators=[DataRequired()])
	submit = SubmitField('Rename')