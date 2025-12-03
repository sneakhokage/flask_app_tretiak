from flask import render_template, redirect, url_for, flash
from sqlalchemy import select  
from . import posts_bp
from app import db
from .models import Post, Tag
from app.forms import PostForm

@posts_bp.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=form.author_id.data,
            created_at=form.posted.data,
            is_active=form.is_active.data
        )

        selected_tags_ids = form.tags.data

        tags_objects = db.session.scalars(
            select(Tag).where(Tag.id.in_(selected_tags_ids))
        ).all()

        new_post.tags = tags_objects

        db.session.add(new_post)
        db.session.commit()
        
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.index'))

    posts = db.session.scalars(select(Post).order_by(Post.created_at.desc())).all()
    
    return render_template('posts/index.html', form=form, posts=posts)