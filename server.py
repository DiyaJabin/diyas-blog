import hashlib
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash,request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm,RegisterForm,LoginForm,CommentForm,ContactForm
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__,instance_path="/tmp/instance")
os.makedirs("/tmp/instance",exist_ok=True)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

# LOGIN SETUP
login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login to access this page.")
    return redirect(url_for('login'))




# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class User(UserMixin,db.Model):
    __tablename__= "user"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str]=mapped_column(String(250),nullable=False)
    email: Mapped[str]=mapped_column(String(250),nullable=False)

    #One user can have many BlogPost objects
    #user.posts will give you all the blog posts written by the user
    #back_populates="author" means this relationship is connected to the 'author' relationship
    #inside the BlogPost class
    posts=relationship("BlogPost",back_populates="author")

    #One user can have many comments; linking rel is author inside Comment
    comments=relationship("Comment",back_populates="author")

    def avatar(self, size=100):
        email = self.email.strip().lower()
        email_hash = hashlib.sha256(email.encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    #Connection to user table through Foreign Keyy
    author_id: Mapped[int]=mapped_column(Integer, ForeignKey('user.id'))

    #This creates the Python Object rel
    #post.author will give the full User object
    #back_populates="posts" connects it to User.posts
    author= relationship("User",back_populates="posts")

    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    #One BlogPost can have many comments
    comments=relationship("Comment",back_populates="parent_blog",cascade="all, delete-orphan")
    #When a blog post is deleted, its comments are also safely deleted

class Comment(db.Model):
    __tablename__="comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str]=mapped_column(Text, nullable=False)

    #Connect to User table with FK
    author_id: Mapped[int]=mapped_column(Integer, ForeignKey('user.id'))
    #Rel to the User Objectt
    author=relationship("User",back_populates="comments")
    #Connect to BlogPost table
    post_id: Mapped[int]=mapped_column(Integer, ForeignKey('blog_posts.id'))
    #Rel to BlogPost object
    parent_blog=relationship("BlogPost",back_populates="comments")

#ForeignKey creates the actual db connection; relationship() creates the Python object connection


with app.app_context():
    db.create_all()

#decorator creation
def admin_only(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please login first")
            return redirect(url_for('login'))
        if current_user.id==1:
            return function(*args,**kwargs)
        return abort(403)
    return decorated_function

@app.route('/register', methods=['GET','POST'])
def register():
    register_form=RegisterForm()
    if request.method=='POST':
        email=request.form['email']
        exists=db.session.execute(db.select(User).where(User.email==email)).scalars().first()
        if exists:
            flash("You've already signed up with that email, login instead")
            return redirect(url_for('login'))
        password=generate_password_hash(
            request.form['password'],
            method='pbkdf2:sha256:600000',
            salt_length=8,
        )
        new_user=User(
            username=request.form['username'],
            password=password,
            email=email,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('get_all_posts'))
    else:
        return render_template("register.html",register_form=register_form)


@app.route('/login',methods=['GET','POST'])
def login():
    login_form=LoginForm()
    if request.method=='POST':
        email=request.form['email']
        check_user=db.session.execute(db.select(User).where(User.email==email)).scalars().first()
        if check_user:
            password=request.form['password']
            if check_password_hash(check_user.password,password):
                login_user(check_user)
                return redirect(url_for('get_all_posts'))
            else:
                flash("Wrong password, try again.")
                return redirect(url_for('login'))
        else:
            flash("User does not exist, please register")
            return redirect(url_for('login'))
    return render_template("login.html",login_form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)



@app.route("/post/<int:post_id>",methods=['GET','POST'])
def show_post(post_id):
    form=CommentForm()
    if request.method=='POST':
        if not current_user.is_authenticated:
            flash("You need to login to comment on a post")
            return redirect(url_for('login'))
        else:
            new_comment=Comment(
                text=request.form['comment'],
                post_id=post_id,
                author_id=current_user.id,
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('show_post',post_id=post_id))
    requested_post = db.get_or_404(BlogPost, post_id)
    comments=requested_post.comments
    return render_template("post.html", post=requested_post,comment_form=form,comments=comments)



@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user._get_current_object(),
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)



@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)



@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact",methods=['GET','POST'])
def contact():
    contact_form=ContactForm()
    if request.method=='POST':
        if not current_user.is_authenticated:
            flash("Please login to contact me")
            return redirect(url_for('login'))
        sender_email=os.getenv('MY_EMAIL')
        receiver_email=os.getenv('MY_EMAIL')
        message=request.form['message']
        content=(f"From: {current_user.username},"
                 f"Email: {current_user.email},"
                 f"Message: {message}")
        with smtplib.SMTP('smtp.gmail.com',587) as server:
            server.starttls()
            server.login(sender_email,os.getenv('PASSWORD'))
            server.sendmail(sender_email, receiver_email, content)
        return render_template("contact.html",form=contact_form,msg_sent=True)
    return render_template("contact.html",form=contact_form,msg_sent=False)


if __name__ == "__main__":
    app.run(debug=False, port=5002)
