from flask import render_template, request, url_for, redirect, session, flash, make_response

from . import users_bp 

from app.forms import LoginForm

@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age")
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    return redirect(url_for(".greetings", name="ADMIN"))

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == 'admin' and password == '12345':
            session['username'] = username
            flash_message = f"Ви успішно увійшли! Опцію 'Запам'ятати мене' {'обрано' if remember else 'не обрано'}."
            flash(flash_message, "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Неправильне ім'я користувача або пароль. Спробуйте ще раз!", "danger")
            
    return render_template('users/login.html', form=form)

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