from flask import Blueprint,render_template,request,redirect,make_response,session,Flask,url_for,send_from_directory
from werkzeug import secure_filename
import pymysql
import hashlib
import xlrd
import os
import math

UPLOAD_FOLDER = '../static/xlsx'
ALLOWED_EXTENSIONS = set(['xlsx'])

systemSet=Blueprint("systemSet",__name__)

def connect():
    db = pymysql.connect('localhost', 'root', '123456', 'jiaowu', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    return db

def addsign(str):
    arr=[]
    for item in str:
        arr.append(item)
    return ",".join(arr)
#分页
def pages(counts,pageNum):
    #couunts总条数，pageNum每页条数
    if request.url.find("?")<0:
        url=request.url+"?page="
    else:
        if request.url.find("page")<0:
            url=request.url+"&page="
        else:
            url=request.url[0:request.url.rfind("=")+1]
    pageCounts=math.ceil(counts/pageNum)
    currentPage=int(request.args.get("page") or 0)
    strs="共%s页" %(pageCounts)
    strs+=" <a href='%s'>首页</a> "%(url+str(0))
    last=currentPage-1 if currentPage-1>0 else 0
    strs+=" <a href='%s'>上一页</a> "%(url+str(last))
    start=currentPage-2 if currentPage-2> 0 else 0
    end=start+4 if currentPage+4<pageCounts else pageCounts
    for item in range(start,end):
        if currentPage==item:
            strs+=" <a href='%s' style='color=red'>%s</a> "%(url+str(item),item+1)
        else:
            strs+=" <a href='%s'>%s</a> "%(url+str(item),item+1)
    next=currentPage+1 if currentPage+1<pageCounts else pageCounts-1
    strs+=" <a href='%s'>下一页</a> "%(url+str(next))
    strs+=" <a href='%s'>尾页</a> "%(url+str(pageCounts-1))
    limit=" limit "+str(currentPage*pageNum)+","+str(pageNum)
    return {'limit':limit,'strs':strs}
# 判断权限,参数需要加双引号
def ispower(powerName,permissionCode):
    result=permissionCode in session.get(powerName).split(",")
    return result
# 修改通知
@systemSet.route('/setNotice61')
def setNotice61():
    result=ispower("setpower","1")
    return render_template('61setNotice.html') if result==True else render_template('nopower.html')
@systemSet.route('/setNotice')
def setNotice():
    content = request.args.get('content')
    date = request.args.get('date')
    updataer = session.get("name")
    db = connect()
    cur = db.cursor()
    cur.execute('insert into notice (content,updataer,date) values (%s,%s,%s)', (content,updataer,date))
    db.commit()
    db.close()
    cur.close()
    return "ok"
# 管理员工具
@systemSet.route('/tool63')
def tool63():
    result=ispower("setpower","3")
    if(result==False):
        return render_template('nopower.html')
    else:
        cls = request.args.get("cls") or "1"
        con = request.args.get("con") or "1"
        if con == "1" and cls != "role":
            cls = "1"
        db = connect()
        cur = db.cursor()
        cur.execute('select id from userinfo where userid is not null and ' + cls + '=%s',(con))
        pag = pages(len(cur.fetchall()), 10)
        lim = pag['limit']
        cur.execute('select id,userid,name,hwpower,stupower,teapower,clspower,filepower,setpower,role from userinfo where userid is not null and '+cls+'=%s'+lim,(con))
        data = cur.fetchall()
        db.commit()
        db.close()
        cur.close()
        for item in data:
            if item["role"]=="0":
                item["role"]="管理员"
            elif item["role"]=="1":
                item["role"]="教师"
            elif item["role"]=="2":
                item["role"]="学生"

        return render_template('63tool.html',results=data,pag=pag)

@systemSet.route('/tooladduser')
def tooladduser():
    result = ispower("setpower", "3")
    return render_template('63tooladduser.html') if result == True else render_template('nopower.html')
@systemSet.route('/add',methods=["POST"])
def add():
    # 账号查重
    userid = request.form["userid"]
    db = connect()
    cur = db.cursor()
    cur.execute('select id from userinfo where userid = %s',(userid))
    result = cur.fetchall()
    db.commit()
    cur.close()
    if result:
        return render_template('400.html')
    else:
        password = request.form["password"]
        md5 = hashlib.md5()
        md5.update(password.encode("utf8"))
        password = md5.hexdigest()

        name = request.form["name"]
        sex = request.form["sex"]
        birthday = request.form["birthday"]
        role = request.form["role"]
        if role=="0":
            hwpower="1,2,3"
            stupower="1,2"
            teapower="1,2,3"
            clspower="1,2,3"
            filepower="1,2"
            setpower="1,2,3"
            cur = db.cursor()
            cur.execute("insert into userinfo (userid,password,name,sex,birthday,role,hwpower,stupower,teapower,clspower,filepower,setpower) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid, password, name, sex, birthday, role, hwpower, stupower, teapower, clspower,filepower, setpower))
        elif role=="1":
            hwpower = "1"
            stupower = "1"
            teapower = "1,2"
            clspower = "1,2"
            filepower = "1"
            setpower = "0"
            subject = request.form["subject"]
            cur = db.cursor()
            cur.execute("insert into userinfo (userid,password,name,sex,birthday,subject,role,hwpower,stupower,teapower,clspower,filepower,setpower) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid, password, name, sex, birthday, subject, role, hwpower, stupower, teapower, clspower,filepower, setpower))
        elif role=="2":
            hwpower = "2,3"
            stupower = "0"
            teapower = "0"
            clspower = "2"
            filepower = "0"
            setpower = "0"
            clas = request.form["class"]
            cur = db.cursor()
            cur.execute("insert into userinfo (userid,password,name,sex,birthday,class,role,hwpower,stupower,teapower,clspower,filepower,setpower) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid, password, name, sex, birthday, clas, role, hwpower, stupower, teapower, clspower,filepower, setpower))

        db.commit()
        db.close()
        cur.close()
        return redirect('/systemSet/tool63')

@systemSet.route('/tooldel')
def tooldel():
    result = ispower("setpower", "3")
    if(result==False):
        return render_template('nopower.html')
    else:
        id = request.args.get("id")
        db = connect()
        cur = db.cursor()
        cur.execute("delete from userinfo where id=%s", (id))
        db.commit()
        db.close()
        cur.close()
        return "ok"
@systemSet.route('/toolupdate')
def toolupdate():
    id=request.args.get("id")
    return render_template('63toolupd.html',id=id)
@systemSet.route('/update/<id>')
def update(id):
    password = request.args.get("password")
    role = request.args.get("role")
    hwpower = addsign(((request.args.get("hwpower1") or "") + (request.args.get("hwpower2") or "") + (request.args.get("hwpower3") or ""))or "0")
    stupower = addsign(((request.args.get("stupower1") or "") + (request.args.get("stupower2") or ""))or "0")
    teapower = addsign(((request.args.get("teapower1") or "") + (request.args.get("teapower2") or "") + (request.args.get("teapower3") or ""))or "0")
    clspower = addsign(((request.args.get("clspower1") or "") + (request.args.get("clspower2") or "") + (request.args.get("clspower3") or ""))or "0")
    filepower = addsign(((request.args.get("filepower1") or "") + (request.args.get("filepower2") or ""))or "0")
    setpower = addsign(((request.args.get("setpower1") or "") + (request.args.get("setpower2") or "") + (request.args.get("setpower3") or ""))or "0")
    db = pymysql.connect('localhost', 'root', 'lll555666', 'jiaowu', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()
    cur.execute('update userinfo set role=%s,hwpower=%s,stupower=%s,teapower=%s,clspower=%s,filepower=%s,setpower=%s where id=%s', (role,hwpower,stupower,teapower,clspower,filepower,setpower,id))
    db.commit()
    if password:
        md5 = hashlib.md5()
        md5.update(password.encode("utf8"))
        password = md5.hexdigest()
        cur.execute('update userinfo set password=%s where id=%s',(password,id))
        db.commit()
    db.close()
    cur.close()
    return redirect('/systemSet/tool63')
@systemSet.route('/toolxlsxadd')
def toolxlsxadd():
    return render_template('63tooladdusers.html')
@systemSet.route("/exceladd",methods=["post"])
def exceladd():
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    file = request.files["file"]
    if file and allowed_file(file.filename):
        file.save("addusers.xlsx")
        book = xlrd.open_workbook("addusers.xlsx")
        sheet = book.sheet_by_index(0)
        datas=[]
        for item in range(1, sheet.nrows):
            arr = sheet.row_values(item)
            arr1 = sheet.row_values(item)
        db = connect()
        cur = db.cursor()
        cur.executemany("insert into userinfo () values()",())
        db.commit()
        return "ok"
@systemSet.route('/download')
def download():
    res = make_response(send_from_directory("C:/Users/62710\Desktop/ribaoguanli/serve/static/xlsx",filename="demo.xlsx", as_attachment=True))
    res.headers["content-disposition"] = "attachment;filename=demo.xlsx"
    return res
