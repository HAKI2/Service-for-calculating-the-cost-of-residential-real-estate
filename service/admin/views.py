import datetime
from flask import (redirect, request, url_for, current_app, make_response, flash)
from service.admin import blueprint
from flask.templating import render_template
from service.database.models import request_pool, segment, wall_material, flat, condition, room_quantity, user
from service.extensions import db
from sqlalchemy import exc
from service.admin.forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user

@blueprint.context_processor
def inject_user():
    return dict(user=current_user)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('excel_import.excel_import'))
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        username = form.data.get('username')
        password = form.data.get('password')
        remember_me = form.data.get('remember_me')
        user_obj = user.query.filter_by(username=username).first()
        if user_obj:
            if user_obj.check_password(password):
                login_user(user_obj, remember=remember_me)
                user_obj.last_login = datetime.datetime.now()
                return redirect(request.args.get('next') or url_for('excel_import.excel_import'))
        error = flash(f'Неверный логин или пароль')
    return render_template('login.html', form=form, error=error)


@login_required
@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('excel_import.excel_import'))
    form = RegistrationForm()
    error = None
    if form.validate_on_submit():
        username = form.data.get('username')
        first_name = form.data.get('first_name')
        last_name = form.data.get('last_name')
        email = form.data.get('email')
        password = form.data.get('password')
        user_obj = user.query.filter_by(username=username).first()
        if not user_obj:
            user_obj = user(username=username, first_name=first_name, last_name=last_name, email=email)
            user_obj.set_password(password)
            db.session.add(user_obj)
            db.session.commit()
            login_user(user_obj)
            return redirect(request.args.get('next') or url_for('excel_import.excel_import'))
        error = flash(f'Пользователь с таким логином уже существует')
    return render_template('signup.html', form=form, error=error)

@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('admin_base.login'))