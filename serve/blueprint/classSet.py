from flask import Blueprint,render_template,request,session
import pymysql
import random
import math

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

classSet=Blueprint("classSet",__name__)

# 判断权限,参数需要加双引号
def ispower(powerName,permissionCode):
    result=permissionCode in session.get(powerName).split(",")
    return result
# 生成随机数
def randomNum(num,len):
    return random.sample(range(1, len), num)

# 查看班级信息
@classSet.route('/classinfo41')
def classinfo41():
    result = ispower("clspower", "1")
    if (result == False):
        return render_template('nopower.html')
    else:
        cls = request.args.get("cls") or "1"
        con = request.args.get("con") or "1"
        if con == "1":
            cls = "1"
        db = pymysql.connect('localhost', 'root', 'lll555666', 'jiaowu', charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        cur.execute('select * from classinfo where classid is not null and ' + cls + '=%s', (con))
        data = cur.fetchall()
        db.commit()
        cur.close()
        for i in range(len(data)):
            cur = db.cursor()
            cur.execute('select userid from userinfo where role=2 and class =%s', (data[i]["class"]))
            pag = pages(len(cur.fetchall()), 5)
            lim = pag['limit']
            cur.execute('select userid from userinfo where role=2 and class =%s'+lim, (data[i]["class"]))
            stu = cur.fetchall()
            cur.close()
            data[i].setdefault("num",str(len(stu)))
        db.close()
        return render_template('41classinfo.html', results=data,pag=pag)
# 修改班级信息
@classSet.route('/setClassinfo43')
def setClassinfo43():
    result = ispower("clspower", "3")
    if (result == False):
        return render_template('nopower.html')
    else:
        cls = request.args.get("cls") or "1"
        con = request.args.get("con") or "1"
        if con == "1":
            cls = "1"
        db = pymysql.connect('localhost', 'root', 'lll555666', 'jiaowu', charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        cur.execute('select * from classinfo where classid is not null and ' + cls + '=%s', (con))
        pag = pages(len(cur.fetchall()), 5)
        lim = pag['limit']
        cur.execute('select * from classinfo where classid is not null and ' + cls + '=%s'+lim, (con))
        data = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        return render_template('43setClassinfo.html', results=data,pag=pag)
@classSet.route('/setClassinfo')
def setClassinfo():
    classid = request.args.get("classid")
    newclass = request.args.get("newclass")
    oldclass = request.args.get("oldclass")
    master = request.args.get("master")
    db = pymysql.connect('localhost', 'root', 'lll555666', 'jiaowu', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()
    cur.execute('select classid from classinfo where class=%s',(newclass))
    result = cur.fetchone()
    db.commit()
    cur.close()
    # 班级重复
    if result:
        cur = db.cursor()
        cur.execute('update classinfo set master=%s where classid=%s', (master, classid))
        db.commit()
        cur.close()
        db.close()
        return "classError"
    # 班级不重复
    else:
        cur = db.cursor()
        cur.execute('update classinfo set class=%s,master=%s where classid=%s', (newclass, master, classid))
        db.commit()
        cur.close()
        cur = db.cursor()
        cur.execute('update userinfo set class=%s where class=%s', (newclass,oldclass))
        db.commit()
        cur.close()
        db.close()
        return "ok"
# 随堂测试
@classSet.route('/test')
def test():
    result = ispower("clspower", "2")
    if (result == False):
        return render_template('nopower.html')
    else:
        db = pymysql.connect('localhost', 'root', 'lll555666', 'jiaowu', charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        cur.execute('select * from papers where type='+"1"+" ORDER BY rand() LIMIT 2")
        result1 = cur.fetchall()
        cur.execute('select * from papers where type=' + "2" + " ORDER BY rand() LIMIT 2")
        result2 = cur.fetchall()
        cur.execute('select * from papers where type=' + "3" + " ORDER BY rand() LIMIT 2")
        result3 = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        return render_template('42paper.html', result1=result1,result2=result2,result3=result3)