from flask import Flask, request
from flask import render_template
from flask_wtf import Form
from wtforms import SelectField, StringField, SubmitField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
import flask_bootstrap

class RegistrationForm(Form):
    loginid = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('enter password', validators=[DataRequired(), Length(min=5,max=20) ])
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    cardetail = StringField('car detail')
    licensedetail = StringField('License detail')
    mobile = IntegerField('mobile', validators=[DataRequired(), Length(min=10, max=10, message="enter a 10 digit valid mobile number")])
    email = StringField('email', validators=[DataRequired(), Email()])
    address = TextAreaField('address', validators=[DataRequired()])
    refralid = IntegerField('refral code')
    submit = SubmitField('Submit')
    sex = SelectField('gender')
    registeredas = SelectField('passenger/owner')



