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
        reg.name = form.name.data
        reg.age = form.age.data
        reg.cardetail = form.cardetail.data
        reg.mobile = form.mobile.data
        reg.email = form.email.data
        reg.address = form.address.data
        reg.referalid = form.refralid.data
        reg.sex = form.sex.data
        reg.registeredas = form.registeredas.data

        db.session.add(reg)
        db.session.commit()

    return render_template('login.html', form=form)

