from datetime import timedelta
import redis
import flask_mail as flaskmail
from pymysql import *

from route.forum import forum
from route.indentify import toi1, toi2,i2Submit

conn = connect(host='localhost', port=3306, user='root', passwd='123', db='tjh', charset='utf8')
cursor = conn.cursor()

from route.login import logIn
from route.register import register
from flask import Flask, request, url_for, render_template, session

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'asd'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# mail和redis配置
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hugh_888@126.com'
app.config['MAIL_PASSWORD'] = 'aut1234'
app.config['FLASK_MAIL_SENDER'] = '皮皮虾！我们走！<hugh_888@126.com>'
app.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[皮皮虾！我们走]'
mail = flaskmail.Mail(app)
redis_store = redis.StrictRedis(host='127.0.0.1', port='6379')


@app.route('/')
def toLogin():
    return render_template('login.html')


@app.route('/reNewPwd.html')
def toReNewPwd():
    return render_template('reNewPwd.html')


@app.route('/index.html')
def toIndex():
    print(session.get('user_id'))
    return render_template('index.html')


@app.route('/information.html')
def toInformation():
    return render_template('/info/information.html')



@app.route('/identify.html')
def toIdentify():
    return render_template('/iden/identify.html')


@app.route('/qv?<int:id>')
def quickView(id):
    sqlStr = "select sneaker_info from sneaker where sneaker_id=" + str(id)  # 数据库操作
    cursor.execute(sqlStr)  # 执行数据库语句
    info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
    strInfo = str(info).replace('(', "").replace("\'", "").replace(",", "").replace(')', "")
    return render_template('/info/qv.html', info=strInfo)




@app.route('/aboutUs.html')
def toAboutUs():
    return render_template('aboutUs.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

forum(app)
logIn(app)
register(app, mail, redis_store)
toi1(app)
toi2(app)
i2Submit(app)

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_info = request.form.to_dict()  # 获取表单内容
        sqlStr = "select sneaker_info from sneaker where sneaker_name like" +"'%"+str(search_info.get("sName"))+"%'" # 数据库操作
        cursor.execute(sqlStr)  # 执行数据库语句
        info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
        strInfo = str(info).replace('(', "").replace("\'", "").replace(",", "").replace(')', "")

        sqlStrOfName = "select sneaker_name from sneaker where sneaker_name like" + "'%" + str(
            search_info.get("sName")) + "%'"  # 数据库操作
        cursor.execute(sqlStrOfName)  # 执行数据库语句
        info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
        strInfo2 = str(info).replace('(', "").replace("\'", "").replace(')', "")
        item=strInfo2.split(",")
        for i in range(len(item)):
            if item[i] is ",":
                item.remove(item(i))
        for i in item:
            if i == '':
                item.remove(i)
        mytest = [i for i in item if i != '']
        print(mytest)
        itemOfPic = mytest.copy()
        itemOfinfo = mytest
        for i in range(len(mytest)):
            if(i!=0):
                itemOfPic[i]=itemOfPic[i][1:len(itemOfPic[i])]
                itemOfPic[i] = itemOfPic[i] + ".jpg"
            else:
                itemOfPic[i]=itemOfPic[i].strip()
                itemOfPic[i]=item[i]+".jpg"

        sqlStr = "select sneaker_info from sneaker where sneaker_name like" + "'%" + str(search_info.get("sName")) + "%'"  # 数据库操作
        sqlStr_shoe = "select sneaker_name from sneaker where sneaker_name like" + "'%" + str(search_info.get("sName")) + "%'"  # 数据库操作
        cursor.execute(sqlStr)  # 执行数据库语句
        info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
        cursor.execute(sqlStr_shoe)  # 执行数据库语句
        info_shoe = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
        print(info)
        print(itemOfPic)
        strInfo1 = str(info).split(",")
        strInfo_shoe = str(info_shoe).split(",")
        for i in range(len(strInfo1)):
            strInfo1[i] = strInfo1[i].replace('(', "").replace("\'", "").replace(')', "")
        for i in range(len(strInfo_shoe)):
            strInfo_shoe[i] = strInfo_shoe[i].replace('(', "").replace("\'", "").replace(')', "")
        mytest2 = [i for i in strInfo1 if i != '']
        mytest3 = [i for i in strInfo_shoe if i != '']
        print(mytest2)
        return render_template('/info/search.html',name=itemOfPic,info=mytest2,shoe=mytest3)

if __name__ == '__main__':
    app.run()
