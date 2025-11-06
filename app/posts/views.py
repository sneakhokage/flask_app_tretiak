from flask import render_template, redirect, url_for, flash, request, make_response
from app import db  
from . import posts_bp
from .models import Post
from app.forms import PostForm
from sqlalchemy import select  

@posts_bp.route('/')
def index():
    """
    Головна сторінка блогу, показує всі пости.
    """
    
    stmt = select(Post).order_by(Post.posted.desc())

    all_posts = db.session.scalars(stmt).all()
    
    return render_template('posts/index.html', posts=all_posts)

@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            category=form.category.data,
            content=form.content.data,
            posted=form.posted.data
        )
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Пост успішно створено!', 'success')
            return redirect(url_for('posts.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Помилка при створенні поста: {e}', 'danger')
    
    return render_template('posts/add_post.html', form=form)

@posts_bp.route('/<int:id>')
def post_detail(id):
    """
    Показує один конкретний пост за його 'id'.
    """

    post = db.get_or_404(Post, id)
    
    return render_template('posts/post_detail.html', post=post)

@posts_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):

    post_to_edit = db.get_or_404(Post, id)
    
    form = PostForm(obj=post_to_edit)
    
    if form.validate_on_submit():
        try:
            post_to_edit.title = form.title.data
            post_to_edit.category = form.category.data
            post_to_edit.content = form.content.data
            post_to_edit.posted = form.posted.data

            db.session.commit()
            flash('Пост успішно оновлено!', 'success')
            return redirect(url_for('posts.post_detail', id=post_to_edit.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Помилка при оновленні поста: {e}', 'danger')
            
    return render_template('posts/add_post.html', form=form, post_to_edit=post_to_edit)

@posts_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):

    post_to_delete = db.get_or_404(Post, id)
    
    form = PostForm() 
    
    if request.method == 'POST':
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Пост успішно видалено.', 'success')
            return redirect(url_for('posts.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Помилка при видаленні поста: {e}', 'danger')
            return redirect(url_for('posts.index'))
            
    return render_template('posts/delete_confirm.html', post=post_to_delete, form=form)