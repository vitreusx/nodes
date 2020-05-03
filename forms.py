from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired


class RenameForm(FlaskForm):
	new_name = StringField('New name', validators=[DataRequired()])
	submit = SubmitField('Rename')
