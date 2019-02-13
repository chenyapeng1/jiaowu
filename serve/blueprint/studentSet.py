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

studentSet=Blueprint("studentSet",__name__)

# 判断权限,参数需要加双引号
def ispower(powerName,permissionCode):
    result=permissionCode in session.get(powerName).split(",")
    return result
# 查看学生信息
@studentSet.route('/stuinfo21')
def stuinfo21():
    result = ispower("stupower", "1")
    if (result == False):
        return render_template('nopower.html')
    else:
        cls = request.args.get("cls") or "1"
        con = request.args.get("con") or "1"
        if con == "1":
            cls = "1"
        db = connect()
        cur = db.cursor()
        cur.execute('select name,userid,sex,birthday,class from userinfo where role=2 and ' + cls + '=%s', (con))
        pag = pages(len(cur.fetchall()), 5)
        lim = pag['limit']
        cur.execute('select name,userid,sex,birthday,class from userinfo where role=2 and ' + cls + '=%s'+lim, (con))
        data = cur.fetchall()
        db.commit()
        db.close()
        cur.close()
        return render_template('21stuinfo.html', results=data,pag=pag)
# 修改学生信息
@studentSet.route('/setStuinfo22')
def setStuinfo22():
    result = ispower("stupower", "2")
    if(result==False):
        return render_template('nopower.html')
    else:
        cls=request.args.get("cls") or "1"
        con=request.args.get("con") or "1"
        if con=="1":
            cls="1"
        db = connect()
        cur = db.cursor()
        cur.execute('select name,userid,sex,birthday,class from userinfo where role=2 and '+cls+'=%s',(con))
        pag = pages(len(cur.fetchall()), 5)
        lim = pag['limit']
        cur.execute('select name,userid,sex,birthday,class from userinfo where role=2 and ' + cls + '=%s'+lim, (con))
        data = cur.fetchall()
        db.commit()
        db.close()
        cur.close()
        return render_template('22setStuinfo.html',results=data,pag=pag)

@studentSet.route('/setStuinfo')
def setStuinfo():
    userid = request.args.get("userid")
    name = request.args.get("name")
    sex = request.args.get("sex")
    birthday = request.args.get("birthday")
    clas = request.args.get("clas")
    db = connect()
    cur = db.cursor()
    cur.execute('select classid from classinfo where class=%s', (clas))
    result = cur.fetchone()
    db.commit()
    cur.close()
    # 有此班级
    if result:
        cur = db.cursor()
        cur.execute('update userinfo set name=%s,sex=%s,birthday=%s,class=%s where userid=%s',
                    (name, sex, birthday, clas, userid))
        db.commit()
        cur.close()
        db.close()
        return "ok"
    # 无此班级
    else:
        cur = db.cursor()
        cur.execute('update userinfo set name=%s,sex=%s,birthday=%s where userid=%s',(name, sex, birthday, userid))
        db.commit()
        cur.close()
        db.close()
        return "classError"
