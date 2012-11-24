from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm, oid, db
from app.models import User, ROLE_USER, ROLE_ADMIN
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return 'Hello, World!'

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template(
        'login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS']
    )

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
