from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired, URL,Email
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")



class RegisterForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    username=StringField("Name",validators=[DataRequired()])
    sign_up=SubmitField("Sign me up!")



class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    login=SubmitField('Login')



class CommentForm(FlaskForm):
    comment=CKEditorField("Comment",validators=[DataRequired()])
    post=SubmitField("Post your comment!")

class ContactForm(FlaskForm):
    message=StringField("Message",validators=[DataRequired()])
    send_message=SubmitField("Send")