import hashlib
import os
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import User
from config import Config


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html")


@app.route('/post/<id>', methods=['GET', 'POST'])
@login_required
def post(id):

    post = Post.query.filter_by(id=id).first()
    post.increment_views()
    db.session.commit()
    likeForm = LikeForm()
    commentForm = CommentForm()
    replyForm = ReplyForm()
    if commentForm.validate_on_submit():
        comment = Comment(
            body=commentForm.comment.data, post=post, author=current_user)
        post.decrement_views()
        db.session.add(comment)
        post.increment_comments_counter()
        db.session.commit()
        flash('Your comment is now live!')
        commentForm.comment.data = ''
        return render_template(
            "post.html",
            title='Post',
            post=post,
            likeForm=likeForm,
            commentForm=commentForm,
            replyForm=replyForm,
            scrollToAnchor=comment.id)
    elif replyForm.validate_on_submit():
        comment = Comment.query.filter_by(id=replyForm.commentId.data).first()
        reply = Reply(
            body=replyForm.reply.data,
            comment=comment,
            author=current_user,
            post=post)
        post.decrement_views()
        db.session.add(reply)
        post.increment_comments_counter()
        db.session.commit()
        flash('Your reply is now live!')
        replyForm.reply.data = ''
        return render_template(
            "post.html",
            title='Post',
            post=post,
            likeForm=likeForm,
            commentForm=commentForm,
            replyForm=replyForm,
            scrollToAnchor=reply.id)
    elif likeForm.validate_on_submit():
        liked = post.liked_by.filter_by(user_id=current_user.id).first()
        if not liked:
            like = Like(author=current_user, post=post)
            post.increment_likes()
            post.decrement_views()
            db.session.commit()
            likeForm.like.data = ''
            flash('Your like is now live!')
        else:
            post.liked_by.remove(liked)
            post.decrement_likes()
            post.decrement_views()
            db.session.commit()
            likeForm.like.data = ''
            flash('Your unlike is now live!')
            print(post.liked_by.filter_by(user_id=current_user.id).first())
        return render_template(
            "post.html",
            title='Post',
            post=post,
            likeForm=likeForm,
            commentForm=commentForm,
            replyForm=replyForm,
            scrollToAnchor='likePost')
    return render_template(
        "post.html",
        title='Post',
        post=post,
        likeForm=likeForm,
        commentForm=commentForm,
        replyForm=replyForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            full_name=form.first_name.data + ' ' + form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        if form.photo.data:
            photo = request.files['photo']
            filename = secure_filename(photo.filename)
            extension = filename.split('.')[1]
            filename = str(
                hashlib.md5(filename.split('.')[0].encode()).hexdigest())
            filename = filename + '.' + extension
            photo.save(
                os.path.join(Config.PROFILE_IMAGE_UPLOAD_FOLDER, filename))
            current_user.image_path = os.path.join(
                Config.PROFILE_IMAGE_ACCESS_PATH, filename)
        db.session.commit()
        flash('Your profile changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        'edit_profile.html', title='Edit Profile', form=form)
