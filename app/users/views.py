import os
from flask import current_app, render_template, request, url_for, redirect, session, flash, make_response
from sqlalchemy import select
from . import users_bp 
from app import db
from app.users.models import User 
from app.forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm
from app import bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime, timezone

@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age")
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    return redirect(url_for(".greetings", name="ADMIN"))

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = RegistrationForm()
    if form.validate_on_submit():
    
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash('Ваш акаунт створено! Тепер ви можете увійти', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = LoginForm() 
    
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.username == form.username.data))

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data) 
            
            flash(f"Вітаю, {user.username}! Ви успішно увійшли.", "success")
 
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash("Неправильне ім'я користувача або пароль.", "danger")
            
    return render_template('users/login.html', form=form)

def save_picture(form_picture):
    filename = secure_filename(form_picture.filename)
    
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', filename)

    output_size = (128, 128)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return filename

@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@users_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
            
        current_user.about_me = form.about_me.data    
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш акаунт було оновлено!', 'success')
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('users/account.html', image_file=image_file, form=form)

@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Ваш пароль успішно змінено!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Невірний поточний пароль.', 'danger')
            
    return render_template('users/change_password.html', form=form)

@users_bp.route('/logout')
def logout():
    logout_user() 
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for('users.login'))

@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        flash("Будь ласка, увійдіть, щоб побачити цю сторінку.", "warning")
        return redirect(url_for('users.login'))
    
    if request.method == 'POST':
        response = make_response(redirect(url_for('users.profile')))
        action = request.form.get('action')

        if action == 'add_cookie':
            key = request.form.get('cookie_key')
            value = request.form.get('cookie_value')
            expires_sec = request.form.get('cookie_expires')
            if key and value:
                max_age = None
                if expires_sec:
                    try:
                        max_age = int(expires_sec)
                    except ValueError:
                        pass
                response.set_cookie(key, value, max_age=max_age)
                flash(f"Кукі '{key}' успішно додано!", "success")

        elif action == 'delete_cookie':
            key = request.form.get('delete_key')
            if key and key in request.cookies:
                response.delete_cookie(key)
                flash(f"Кукі '{key}' успішно видалено!", "success")
        
        elif action == 'delete_all_cookies':
            cookies_keys = request.cookies
            for key in cookies_keys:
                if key != 'session':
                    response.delete_cookie(key)
            flash("Всі кукі (окрім сесії) видалено.", "info")
        
        return response
    
    all_cookies = request.cookies
    return render_template('users/profile.html', cookies=all_cookies)

@users_bp.route('/set_theme')
def set_theme():
    theme = request.args.get('theme')
    response = make_response(redirect(url_for('users.profile')))
    if theme in ['light', 'dark']:
        response.set_cookie('theme', theme, max_age=31536000)
        flash(f"Тему змінено на '{theme}'", "success")
    return response

@users_bp.route('/users')
@login_required
def users_list():
    users = db.session.scalars(select(User)).all()
    count = len(users)
    return render_template('users/users_list.html', users=users, count=count)