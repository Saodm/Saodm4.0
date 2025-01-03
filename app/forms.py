from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    description = TextAreaField('描述')
    photo = FileField('上传图片', validators=[FileRequired()])
    submit = SubmitField('发布')

class CommentForm(FlaskForm):
    body = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField('提交')

class SearchForm(FlaskForm):
    query = StringField('搜索', validators=[DataRequired()])
    submit = SubmitField('搜索')