from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired


class RenameForm(FlaskForm):
	new_name = StringField('New name', validators=[DataRequired()])
	submit = SubmitField('Rename')


class ChangePortForm(FlaskForm):
	new_port = IntegerField('New port', validators=[DataRequired()])
	submit = SubmitField('Change')


class AddKnownNodeForm(FlaskForm):
	node_name = StringField('Name', validators=[DataRequired()])
	node_ip = StringField('IP', validators=[DataRequired()])
	node_port = IntegerField('Port', validators=[DataRequired()])
	submit = SubmitField('Add')


class RemoveKnownNodeForm(FlaskForm):
	node_name = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Remove')