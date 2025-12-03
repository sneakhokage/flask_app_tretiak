from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class CourseForm(FlaskForm):
    title = StringField('Назва курсу', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Опис', validators=[DataRequired()])
    price = FloatField('Ціна ($)', validators=[DataRequired(), NumberRange(min=0)])
    duration_hours = IntegerField('Тривалість (годин)', validators=[NumberRange(min=0)])

    category_id = SelectField('Категорія', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Зберегти')

class CourseSearchForm(FlaskForm):
    query = StringField('Пошук курсів', validators=[Length(max=100)])
    submit = SubmitField('Знайти')