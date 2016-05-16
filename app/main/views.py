from flask import Flask, render_template, request
from .. import app, db
from ..tables import Registration
from forms import RegistrationForm

@app.route('/login', methods= ['GET', 'POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        reg = Registration()
        reg.loginid = form.loginid.data
        reg.password = form.password.data
        db.session.add(reg)
        db.session.commit()
    return render_template('login.html', form=form)
