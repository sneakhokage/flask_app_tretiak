from flask import Blueprint, render_template, request, redirect, url_for, flash, session

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

@users_bp.route('/profile')
def profile():
    """Сторінка профілю користувача."""
    if 'username' in session:
        return render_template('users/profile.html')
    else:
        flash("Будь ласка, увійдіть, щоб побачити цю сторінку.", "warning")
        return redirect(url_for('users.login'))