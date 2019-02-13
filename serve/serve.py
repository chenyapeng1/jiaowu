from flask import Flask,render_template,request,redirect,make_response,session
import pymysql
import hashlib
from code import code
# 蓝图
from blueprint.homeworkSet import homeworkSet
from blueprint.studentSet import studentSet
from blueprint.teacherSet import teacherSet
from blueprint.classSet import classSet
from blueprint.fileSet import fileSet
from blueprint.systemSet import systemSet

app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key="123456"
# 注册蓝图
app.register_blueprint(homeworkSet,url_prefix="/homeworkSet")
app.register_blueprint(studentSet,url_prefix="/studentSet")
app.register_blueprint(teacherSet,url_prefix="/teacherSet")
app.register_blueprint(classSet,url_prefix="/classSet")
app.register_blueprint(fileSet,url_prefix="/fileSet")
app.register_blueprint(systemSet,url_prefix="/systemSet")

def connect():
    db = pymysql.connect('localhost', 'root', '123456', 'jiaowu', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    return db

# 错误
@app.errorhandler(404)
def error(error):
    return render_template('404.html')

# 权限错误
@app.route('/nopower')
def nopower():
    return render_template('nopower.html')
# 操作成功和失败
@app.route('/success')
def success():
    return render_template('success.html')
@app.route('/error')
def err():
    return render_template('400.html')
# 访问根目录
@app.route('/')
def index():
    if(session.get("login")=="yes"):
        db = connect()
        cur = db.cursor()
        cur.execute('select * from notice order by id desc limit 1')
        result = cur.fetchone()
        if (result):
            notice = result["content"]
            day = result["date"]
        else:
            notice = ""
            day = "无通知"
        db.commit()
        db.close()
        cur.close()
        res=make_response(render_template('index.html',data={'name':session.get('name'),'notice':notice,'day':day}))
        return res
    else:
        return  redirect('/login')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/codeimg')
def codeimg():
    codeobj=code()
    res=make_response(codeobj.output())
    session["code"]=codeobj.str.lower()
    res.headers["content-type"]="image/png"
    return res
# 验证登录
@app.route('/checklogin',methods=["POST"])
def checklogin():
    if (session.get("code") == request.form["code"].lower()):
        db = connect()
        cur = db.cursor()

        userid=request.form["userid"]
        upass=request.form["password"]

        md5=hashlib.md5()
        md5.update(upass.encode("utf8"))
        upass=md5.hexdigest()
        cur.execute('select * from userinfo where userid=%s and password=%s',(userid,upass))
        result=cur.fetchone()
        db.commit()

        db.close()
        cur.close()

        if(result):
            res = make_response(redirect('/'))
            # 登录状态
            session["login"]="yes"
            # 用户ID
            session["userid"]=str(result["userid"])
            # 用户名
            session["name"]=result["name"]
            # 用户权限
            session["hwpower"] = str(result["hwpower"])
            session["stupower"] = str(result["stupower"])
            session["teapower"] = str(result["teapower"])
            session["clspower"] = str(result["clspower"])
            session["filepower"] = str(result["filepower"])
            session["setpower"] = str(result["setpower"])
            return res
        else:
            return redirect('/login')
    else:
        return redirect('/login')
# 退出登录
@app.route('/logout')
def logout():
    res = make_response(redirect('/'))
    session.pop("login")
    session.pop("userid")
    session.pop("hwpower")
    session.pop("stupower")
    session.pop("teapower")
    session.pop("clspower")
    session.pop("filepower")
    session.pop("setpower")
    session.pop("code")
    return res
# 修改密码
@app.route('/myinfo')
def myinfo():
    return render_template('setPassword.html')
@app.route('/setPassword',methods=["POST"])
def setPassword():
    password = request.form["password"]
    md5 = hashlib.md5()
    md5.update(password.encode("utf8"))
    password = md5.hexdigest()
    userid=session.get('userid')
    db = connect()
    cur = db.cursor()
    cur.execute('select * from userinfo where userid=%s and password=%s', (userid, password))
    result = cur.fetchone()
    db.commit()
    db.close()
    cur.close()
    if(result):
        db = connect()
        cur = db.cursor()
        newpassword = request.form["inputPassword2"]
        md5 = hashlib.md5()
        md5.update(newpassword.encode("utf8"))
        newpassword = md5.hexdigest()
        cur.execute('update userinfo set password=%s where userid=%s', (newpassword, userid))
        db.commit()
        db.close()
        cur.close()
        return render_template('success.html')
    else:
        return render_template('400.html')

if __name__ == "__main__":
    app.run()
