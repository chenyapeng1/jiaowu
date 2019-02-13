from flask import Blueprint,render_template,request,redirect,make_response,session,Flask
import pymysql
import math

def connect():
    db = pymysql.connect('localhost', 'root', '123456', 'jiaowu', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    return db

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

homeworkSet=Blueprint("homeworkSet",__name__)

# 判断权限,参数需要加双引号
def ispower(powerName,permissionCode):
    result=permissionCode in session.get(powerName).split(",")
    return result
# 查看作业
@homeworkSet.route('/homework11')
def homework11():
    result = ispower("hwpower", "1")
    if (result == False):
        return render_template('nopower.html')
    else:
        cls = request.args.get("cls") or "1"
        con = request.args.get("con") or "1"
        if con == "1":
            cls = "1"
        db = connect()
        cur = db.cursor()
        cur.execute('select * from homework where id is not null and ' + cls + '=%s', (con))
        pag=pages(len(cur.fetchall()), 5)
        lim=pag['limit']
        cur.execute('select * from homework where id is not null and ' + cls + '=%s'+lim, (con))
        data = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        return render_template('11homework.html', results=data,pag=pag)
@homeworkSet.route('/homework')
def homework():
    id = request.args.get("id")
    db = connect()
    cur = db.cursor()
    cur.execute('select * from homework where id =%s', (id))
    data =cur.fetchone()
    db.commit()
    cur.close()
    db.close()
    return render_template('11thework.html', results=data)

# 上交作业
@homeworkSet.route('/addHomework12')
def addHomework12():
    result = ispower("hwpower", "2")
    if (result == False):
        return render_template('nopower.html')
    else:
        userid=session.get("userid")
        db = connect()
        cur = db.cursor()
        cur.execute('select userid,class,name from userinfo where userid =%s', (userid))
        data = cur.fetchone()
        db.commit()
        cur.close()
        db.close()
        return render_template('12addHomework.html', results=data)
@homeworkSet.route('/addHomework')
def addHomework():
    userid = request.args.get("userid")
    name = request.args.get("name")
    title = request.args.get("title")
    uptime = request.args.get("uptime")
    text = request.args.get("text")
    clas = request.args.get("clas")
    db = connect()
    cur = db.cursor()
    cur.execute("insert into homework (userid,name,title,text,uptime,class) values (%s,%s,%s,%s,%s,%s)",(userid,name,title,text,uptime,clas))
    db.commit()
    db.close()
    cur.close()
    return "ok"
# 修改本用户作业
@homeworkSet.route('/updHomework13')
def updHomework13():
    result = ispower("hwpower", "3")
    if (result == False):
        return render_template('nopower.html')
    else:
        userid = session.get("userid")
        cls = request.args.get("cls") or "1"
        con = request.args.get("con") or "1"
        if con == "1":
            cls = "1"
        db = connect()
        cur = db.cursor()
        cur.execute('select * from homework where userid =%s and ' + cls + '=%s', (userid,con))
        pag = pages(len(cur.fetchall()), 5)
        lim = pag['limit']
        cur.execute('select * from homework where userid =%s and ' + cls + '=%s'+lim, (userid, con))
        data = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        return render_template('13updHomework.html', results=data,pag=pag)

@homeworkSet.route('/delHomework')
def delHomework():
    result = ispower("hwpower", "3")
    if (result == False):
        return render_template('nopower.html')
    else:
        id = request.args.get("id")
        db = connect()
        cur = db.cursor()
        cur.execute('delete from homework where id =%s', (id))
        db.commit()
        cur.close()
        db.close()
        return redirect('homeworkSet/updHomework13')

@homeworkSet.route('/updtheHomework')
def updHomework():
    result = ispower("hwpower", "3")
    if (result == False):
        return render_template('nopower.html')
    else:
        id = request.args.get("id")
        db = connect()
        cur = db.cursor()
        cur.execute('select * from homework where id =%s', (id))
        datas = cur.fetchone()
        db.commit()
        cur.close()
        db.close()
        return render_template("13thework.html",results=datas)
@homeworkSet.route('/upd')
def upd():
    id = request.args.get("id")
    title = request.args.get("title")
    text = request.args.get("text")
    print(id,title,text)
    db = connect()
    cur = db.cursor()
    cur.execute("update homework set title=%s,text=%s where id=%s",(title,text,id))
    db.commit()
    db.close()
    cur.close()
    return "ok"

# @app.route("/upload",methods=["POST"])
# def upload():
#     res=request.files["upload"]
#     reslpath="/static/upload/"+str(random.randint(1,20000))+res.filename.rsplit(".")[1]
#     res.save("."+reslpath)
#     return json.dumps({"uploaded":True,"url":reslpath})



