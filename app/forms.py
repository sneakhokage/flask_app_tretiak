from flask_wtf import FlaskForm

from sqlalchemy import select
from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField, DateTimeLocalField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, Regexp, email
from wtforms.fields import DateField
from datetime import datetime

CATEGORIES = [
    ('General', 'Загальне'),
    ('Technology', 'Технології'),
    ('News', 'Новини'),
    ('Personal', 'Особисте')
]

class ContactForm(FlaskForm):
    """
    Клас форми для сторінки контактів.
    
    """

    name = StringField('Name', validators=[
        DataRequired(message="Це поле є обов'язковим."),
        Length(min=4, max=10, message="Поле має бути довжиною від 4 до 10 символів.")
    ])

    email = StringField('Email', validators=[
        DataRequired(message="Це поле є обов'язковим."),
        Email(message="Введіть коректну email адресу.")
    ])
    phone = StringField('Phone', validators=[
        Regexp(r'^\+380\d{9}$', message="Формат номеру має бути: +380XXXXXXXXX")
    ])
    subject = SelectField('Subject', choices=[
        ('general', 'Загальне питання'),
        ('support', 'Технічна підтримка'),
        ('feedback', 'Відгук про сайт')
    ], validators=[DataRequired(message="Будь ласка, оберіть тему.")])
    message = TextAreaField('Message', validators=[
        DataRequired(message="Це поле є обов'язковим."),
        Length(max=500, message="Повідомлення не може перевищувати 500 символів.")
    ])
    submit = SubmitField('Send')

class LoginForm(FlaskForm):
    """
    Клас форми для сторінки входу.
    """
    username = StringField('Username', validators=[
        DataRequired(message="Це поле є обов'язковим.")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Це поле є обов'язковим."),
        Length(min=4, max=10, message="Поле має бути довжиною від 4 до 10 символів.")
    ])
    
    remember = BooleanField("Запам'ятати мене")
    
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    is_active = BooleanField('Is Active')
    posted = DateField('Publish Date', format='%Y-%m-%d', default=datetime.today, validators=[DataRequired()])
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    author_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField('Save Post')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from app import db
        from app.users.models import User
        from app.posts.models import Tag 
        
        with db.session() as session:

            users = session.scalars(select(User).order_by(User.id)).all()
            self.author_id.choices = [(user.id, user.username) for user in users]

            tags = session.scalars(select(Tag).order_by(Tag.name)).all()
            self.tags.choices = [(tag.id, tag.name) for tag in tags]