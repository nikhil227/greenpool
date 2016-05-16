from flask import Flask, request
from flask import render_template
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
import flask_bootstrap

class RegistrationForm(Form):
    loginid = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('enter password', validators=[DataRequired(), Length(min=5,max=20) ])
    submit = SubmitField('Submit')



