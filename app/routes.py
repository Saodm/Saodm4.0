import os
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm, SearchForm
from app.models import User, Post, Comment, Like

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = PostForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        post = Post(
            title=form.title.data,
            description=form.description.data,
            image_path=filename,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('发布成功！')
        return redirect(url_for('index'))
    return render_template('upload.html', form=form)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('评论已提交！')
        return redirect(url_for('post', post_id=post.id))
    comments = post.comments.order_by(Comment.timestamp.asc())
    return render_template('post.html', post=post, form=form, comments=comments)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('你没有权限删除此帖子。')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('帖子已删除。')
    return redirect(url_for('index'))

@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    if post.likes.filter_by(user_id=current_user.id).first():
        flash('你已经点赞过了！')
    else:
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        flash('点赞成功！')
    return redirect(url_for('index'))

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc())
    return render_template('user.html', user=user, posts=posts)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search_results', query=form.query.data))
    return render_template('search.html', form=form)

@app.route('/search_results/<query>')
def search_results(query):
    posts = Post.query.filter(Post.title.contains(query) | Post.description.contains(query)).all()
    return render_template('search_results.html', query=query, posts=posts)