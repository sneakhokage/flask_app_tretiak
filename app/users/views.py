from flask import render_template, request, url_for, redirect, session, flash, make_response
from sqlalchemy import select

from . import users_bp 
from app import db
from app.users.models import User 
from app.forms import LoginForm, RegistrationForm
from app import bcrypt

@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age")
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    return redirect(url_for(".greetings", name="ADMIN"))

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('users.profile'))

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
    if 'username' in session:
        return redirect(url_for('users.account'))

    form = LoginForm() 
    
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.username == form.username.data))

        if user and user.check_password(form.password.data):
            session['username'] = user.username 
            
            flash_message = f"Вітаю, {user.username}! Ви успішно увійшли"
            flash(flash_message, "success")

            return redirect(url_for('users.account'))
        else:
            flash("Неправильне ім'я користувача або пароль.", "danger")
            
    return render_template('users/login.html', form=form)

@users_bp.route('/account')
def account():
    if 'username' not in session:
        flash("Будь ласка, увійдіть, щоб переглянути цю сторінку.", "warning")
        return redirect(url_for('users.login'))

    username = session['username']
    user = db.session.scalar(select(User).where(User.username == username))
    
    email = user.email if user else "Невідомо"
    
    return render_template('users/account.html', username=username, email=email)


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

@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for('users.login'))

@users_bp.route('/set_theme')
def set_theme():
    theme = request.args.get('theme')
    response = make_response(redirect(url_for('users.profile')))
    if theme in ['light', 'dark']:
        response.set_cookie('theme', theme, max_age=31536000)
        flash(f"Тему змінено на '{theme}'", "success")
    return response

@users_bp.route('/users')
def users_list():
    users = db.session.scalars(select(User)).all()
    count = len(users)
    
    return render_template('users/users_list.html', users=users, count=count)