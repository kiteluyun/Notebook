from flask import Flask,redirect,request,render_template,url_for,session,flash
from passlib.hash import sha256_crypt
from functools import wraps
from setting import Config,db
from forms import RegisterForm,ArticleForm,Login_Form
from model import User,Article,manger_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, current_user
import math
app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login = LoginManager(app)
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('manger'))
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('manger'))
admin = Admin(app, name='读书笔记后台管理', index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Article, db.session))
@login.user_loader
def load_user(manger_user_id):  # 创建用户加载回调函数，接受用户id作为参数
    user = manger_user.query.get(int(manger_user_id))  # 通过user id在数据库中查询
    return user  # 返回用户对象
@app.route('/manger', methods=['GET', 'POST'])
def manger():
    if request.method == "GET":
        # 如果已经登录的话，直接重定向到admin页面
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            form = Login_Form()
            return render_template("manger.html",form=form)
    elif request.method == "POST":
        form = Login_Form(request.form)
        if form.validate():
            username = request.form['username']
            password = request.form['password']
            # 检查数据库里面是否有对应的账密
            result = manger_user.query.filter(manger_user.name == username,manger_user.pwd == password).first()
            if result:
                login_user(result)
                flash("管理员登录成功！")
                return redirect('/admin')
        flash("没有相关的用户名和密码！")
        return render_template("manger.html",form=form)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/dashbord')
def dashbord():
    return render_template('dashbord.html')
#如果用户已经登录
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session: #判断用户是否登录
            return f(*args, **kwargs) #如果登录，则继续执行被装饰函数
        else:                          #如果未登录，则提示无权访问
            flash('无权访问，请先登录')
            return redirect(url_for('login'))
    return wrap


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # 实例化表单类
    if request.method == 'POST'and form.validate():
        #获取字段内容
        username = request.form.get('username')
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
        else:
            email = request.form.get('email')
            password=sha256_crypt.encrypt(str(request.form.get('password')))# 对密码进行加密username
            user = User(email=email,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            flash('您已注册成功，请先登录')  # 闪存信息return redirect(urlfor('login'))#跳转到登录页面
        return redirect(url_for('login'))  # 跳转到登录页面
    return render_template('register.html',form=form)#渲染模板

#返回登录页
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('您已成功退出')# 闪存信息
    return redirect(url_for('login'))#跳转到登录页面


#登录页
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "logged_in" in session: #如果已经登录，则直接跳转到控制台
        return redirect(url_for ("dashboard"))
    if "logged_in" not in session and  request.method == 'POST':  # 如果提交表单
        # 从表单中获取字段
        username = request.form.get('username')
        password_candidate = request.form.get('password')
        result = User.query.filter_by(username=username).first()
        if result:#如果查到记录
            password = result.password  # 获取数据库中的密码
            # 对比用户填写的密码和数据库中的记录密码是否一致
            if sha256_crypt.verify(password_candidate,password):  # 调用verify方法验证，如果为真，则验证通过
# 写入session
                session['logged_in'] = True #登录标记
                session['username'] = username
                session['user_id'] = result.id
                flash('登录成功!')#闪存信息
                # return '登陆成功'
                return redirect(url_for('dashboard'))
            else:
                error ='用户名和密码不匹配'
                return render_template('login.html',error=error)#跳转到登录页，并提示错误信息
        else:
            error = '用户名不存在'
            return render_template('login.html', error=error)
    return render_template('login.html')


# 文章列表
@app.route('/articles')
def list():
    # 获取所有文章
    result = Article.query.order_by().limit(5)
    num = Article.query.count()
    total = math.ceil(num / 10)
    return render_template('articles.html', articles=result,page=1,total=total)
#文章列表分页
@app.route('/page/articles/<int:page>')
def paginates(page):
    # article = Article()
    num = Article.query.count()
    result = Article.query.order_by(Article.id.asc()).paginate(page=page, per_page=5)
    total = math.ceil(num/10)
    return render_template('articles.html', articles=result,page=page,total=total)
# 文章详情
@app.route('/page/articles/article/<string:id>/')
def detail(id):
    # 获取文章详情
    result = Article.query.filter_by(id=id).first()
    return render_template('article.html', article=result)

#控制台
@app.route('/dashboard')
@is_logged_in
def dashboard():
    result = Article.query.order_by().limit(10).all()
    num = Article.query.count()
    total = math.ceil(num/10)
    return render_template('dashbord.html',articles=result,page=1,total=total)

#控制台分页
@app.route('/page/<int:page>')
@is_logged_in
def paginate(page):
    num = Article.query.count()
    result = Article.query.order_by().paginate(page=page, per_page=10)
    total = math.ceil(num/10)
    return render_template('dashbord.html', articles=result,page=page,total=total)

#删除
@app.route('/delete/<string:id>',methods=['POST','GET'])
@is_logged_in
def delete_article(id):
    # 获取要删除的文章
    article = Article.query.filter_by(id=id).first()
    db.session.delete(article)
    db.session.commit()
    flash('文章删除成功')
    return redirect(url_for('dashboard'))

#添加
@app.route('/add_article',methods=['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm()
    if request.method == 'POST' and form.validate():
        article = Article(title=form.title.data,content=form.content.data ,author=session.get('username'),author_id=session.get('user_id'))
        db.session.add(article)
        db.session.commit()
        flash('文章添加成功')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html',form=form)

#编辑
@app.route('/page/edit_article/<int:id>',methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    art=Article.query.get(id)
    if not art:
        flash('ID错误','danger')
        return redirect(url_for('dashboard'))
    form = ArticleForm(request.form)
    if request.method=='POST'and form.validate():
        title=request.form['title']
        content=request.form['content']
        art.title=title
        art.content=content
        db.session.commit()
        flash('文章编辑成功')
        return redirect(url_for('dashboard',id=id))
    form.title.data = art.title
    form.content.data = art.content
    return render_template('edit_article.html',form=form)
if __name__ == '__main__':
    app.run(debug=True)