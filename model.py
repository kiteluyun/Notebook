# from numpy import unicode
from passlib.utils import unicode

from setting import db
from datetime import datetime

class manger_user(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    pwd = db.Column(db.String(120), nullable=False)
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)
    def __repr__(self):
        return '<User %r>' % (self.name)
class User(db.Model):
    #__tablename__ = 'User' #指定当前模型映射的表名
    #创建属性，也就是映射表中的字段/列
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(120), nullable=False)
    #添加关联属性User表关联Article
    #art属性，是user表关联article的数据，user.art返回一个用户对应的所有文章列表数据
    #user引用，是article表关联user的数据 article.user返回一个文章所属的用户数据
    art = db.relationship('Article',backref='user')


class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    author = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_date = db.Column(db.DateTime,nullable=False,default=datetime.now())
    #创建外键
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))











