from flask_wtf import FlaskForm
from wtforms import ValidationError, fields
from wtforms import StringField, PasswordField, SubmitField, TextAreaField,EmailField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class Login_Form(FlaskForm):
    username = StringField(
        '用户名',
        validators=[DataRequired(message="用户名不能为空！"),
                    Length(min=3, max=15, message="用户名长度在3到15个字符之间！")],
        render_kw={"placeholder": "输入用户名", "required": False}
    )
    password = PasswordField(
        '密码', render_kw={"placeholder": "输入密码", "required": False},
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=6, max=20, message='长度在6-20个字符之间'),
        ]
    )
class RegisterForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[DataRequired(message="用户名不能为空！"),
                    Length(min=3, max=15, message="用户名长度在3到15个字符之间！")],
        render_kw={"placeholder": "输入用户名", "required": False}
    )
    email = StringField(
        '邮箱',render_kw={"required" : False},
        validators = [
            DataRequired(message="邮箱不能为空")
        ]
    )
    password = PasswordField(
        '密码',render_kw={ "placeholder": "输入密码","required" : False},
        validators = [
            DataRequired(message='密码不能为空'),
            Length(min=6,max=20,message='长度在6-20个字符之间'),
        ]
    )
    confirm = PasswordField(
        '确认密码',render_kw={"required" : False},
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=6, max=20),
            EqualTo('password', message='两次输入密码不一致')
        ]
    )

class ArticleForm(FlaskForm):
    title = StringField('标题',render_kw={"required" : False,'class':'form-control'},
        validators=[
            DataRequired(message='标题不能为空'),
        ]
    )
    content = TextAreaField(
        '内容',render_kw={"required" : False,'class':'form-control content-text','id':'Text'},
        validators=[
            DataRequired(message='内容不能为空')
        ]
    )