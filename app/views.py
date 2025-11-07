from flask import render_template, request, flash, redirect, url_for, Blueprint
from app.forms import ContactForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('resume.html')

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    
    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
  
        flash(f'Дякуємо за звернення, {name}! Ми отримали ваше повідомлення.', 'success')
 
        return redirect(url_for('main.contacts'))

    return render_template('contacts.html', title='Контакти', form=form)