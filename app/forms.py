from flask_wtf import FlaskForm

from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField

from wtforms.validators import DataRequired, Email, Length, Regexp, email

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
    """
    Клас форми для створення та редагування поста.
    """
    title = StringField('Title', validators=[
        DataRequired(message="Це поле є обов'язковим.")
    ])

    content = TextAreaField('Content', validators=[
        DataRequired(message="Це поле є обов'язковим.")
    ])

    submit = SubmitField('Save Post')