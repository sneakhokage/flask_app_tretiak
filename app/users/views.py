from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', '')
    return render_template('users/hi.html', name=name, age=age)

@users_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='Administrator', age=45))

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Обробляє GET (показ форми) та POST (вхід) запити."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '12345':
            session['username'] = username
            flash("Ви успішно увійшли!", "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Неправильне ім'я користувача або пароль. Спробуйте ще раз", "danger")
            return redirect(url_for('users.login'))
    return render_template('users/login.html')

@users_bp.route('/logout')
def logout():
    """Видаляє користувача з сесії."""
    session.pop('username', None)
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for('users.login'))

@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Сторінка профілю користувача (також обробляє cookies)."""
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
            if key:
                if key in request.cookies:
                    response.delete_cookie(key)
                    flash(f"Кукі '{key}' успішно видалено!", "success")
                else:
                    flash(f"Кукі '{key}' не знайдено!", "warning")

        elif action == 'delete_all_cookies':
            cookies_keys = request.cookies
            for key in cookies_keys:
                if key != 'session':
                    response.delete_cookie(key)
            flash("Всі кукі (окрім сесії) видалено.", "info")

        return response
    all_cookies = request.cookies
    return render_template('users/profile.html', cookies=all_cookies)