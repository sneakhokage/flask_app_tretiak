from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import select, or_
from . import it_courses_bp
from .models import Course, CourseCategory
from .forms import CourseForm, CourseSearchForm
from app import db

@it_courses_bp.route('/', methods=['GET'])
def index():
    search_form = CourseSearchForm(request.args)
    query = select(Course).order_by(Course.created_at.desc()) 

    if search_form.query.data:
        search_query = f"%{search_form.query.data}%"
        query = query.where(or_(
            Course.title.ilike(search_query),
            Course.description.ilike(search_query)
        ))

    courses = db.session.scalars(query).all()
    return render_template('it_courses/index.html', courses=courses, search_form=search_form)

@it_courses_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CourseForm()
    form.category_id.choices = [(c.id, c.name) for c in db.session.scalars(select(CourseCategory)).all()]

    if form.validate_on_submit():
        new_course = Course(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            duration_hours=form.duration_hours.data,
            category_id=form.category_id.data,
            user_id=current_user.id  
        )
        db.session.add(new_course)
        db.session.commit()
        flash('Курс успішно створено!', 'success')
        return redirect(url_for('it_courses.index'))

    return render_template('it_courses/create_update.html', form=form, title="Створити курс")

@it_courses_bp.route('/<int:id>')
def detail(id):
    course = db.session.get(Course, id)
    if not course:
        abort(404)
    return render_template('it_courses/detail.html', course=course)

@it_courses_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    course = db.session.get(Course, id)
    if not course:
        abort(404)
  
    if course.user_id != current_user.id:
        abort(403) 

    form = CourseForm(obj=course) 
    form.category_id.choices = [(c.id, c.name) for c in db.session.scalars(select(CourseCategory)).all()]

    if form.validate_on_submit():
        form.populate_obj(course) 
        db.session.commit()
        flash('Курс оновлено!', 'success')
        return redirect(url_for('it_courses.detail', id=course.id))

    return render_template('it_courses/create_update.html', form=form, title="Редагувати курс")

@it_courses_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    course = db.session.get(Course, id)
    if not course:
        abort(404)

    if course.user_id != current_user.id:
        abort(403)

    db.session.delete(course)
    db.session.commit()
    flash('Курс видалено.', 'info')
    return redirect(url_for('it_courses.index'))