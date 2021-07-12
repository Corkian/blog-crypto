from flask import render_template, url_for, redirect, Blueprint
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from webapp import db
from webapp.db_models import User
from webapp.users.forms import RegisterForm, LoginForm

users_bp = Blueprint('users', __name__)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('users.view'))
        else:
            invalid = True
            return render_template('login.html', invalid=invalid, form=form)

    return render_template('login.html', form=form)


@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('newuser.html')

    return render_template('signup.html', form=form)


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users_bp.route('/view')
@login_required
def view():
    return render_template('view.html', values=User.query.all())
