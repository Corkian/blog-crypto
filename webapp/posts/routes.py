from flask import render_template, redirect, url_for, request, Blueprint
from datetime import datetime
from webapp import db
from webapp.db_models import Blogpost


posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts')
def view_posts():
    all_posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('posts.html', posts=all_posts)


@posts_bp.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)


@posts_bp.route('/addpost', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        author = request.form['author']
        content = request.form['content']

        post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.view_posts'))
    return render_template('add.html')