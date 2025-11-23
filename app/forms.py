from flask_wtf import FlaskForm

from sqlalchemy import select
from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField, DateTimeLocalField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
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

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=14, message="Ім'я користувача має бути від 4 до 14 символів."),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Введіть коректну email адресу.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Пароль має бути мінімум 6 символів.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Паролі повинні співпадати.')
    ])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        from app import db
        from app.users.models import User
        from sqlalchemy import select

        user = db.session.scalar(select(User).where(User.username == field.data))
        if user:
            raise ValidationError('Таке ім\'я користувача вже зайняте.')

    def validate_email(self, field):
        from app import db
        from app.users.models import User
        from sqlalchemy import select

        user = db.session.scalar(select(User).where(User.email == field.data))
        if user:
            raise ValidationError('Ця електронна пошта вже зареєстрована.')

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