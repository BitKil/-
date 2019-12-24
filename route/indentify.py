from flask import request, render_template, session, make_response, flash, redirect, url_for
from pymysql import *
from werkzeug.security import check_password_hash

conn = connect(host='localhost', port=3306, user='root', passwd='123', db='tjh', charset='utf8')
cursor = conn.cursor()


def toi1(app):
    @app.route('/i1.html', methods=['POST', 'GET'])
    def i1():
        if request.method == 'GET':
            if session.get('user_id') is None:
                flash("请登录后操作")
                return redirect(url_for('toIdentify'))
            sqlStr = "select isIdentify from user WHERE user_id =" + "'" + session.get('user_id') + "'"
            cursor.execute(sqlStr)  # 执行数据库语句
            info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
            strInfo1 = str(info).replace('(', "").replace("\'", "").replace(')', "").replace(",", "")
            if int(strInfo1) == 0:
                flash("请先成为鉴定师！")
                return redirect(url_for('toIdentify'))
            else:
                return render_template('/iden/i1.html')
        else:
            return render_template('/iden/i1.html')


def toi2(app):
    @app.route('/i2.html', methods=['POST', 'GET'])
    def i2():
        if request.method == 'GET':
            if session.get('user_id') is None:
                flash("请登录后操作")
                return redirect(url_for('toIdentify'))
            sqlStr = "select isIdentify from user WHERE user_id =" + "'" + session.get('user_id') + "'"
            cursor.execute(sqlStr)  # 执行数据库语句
            info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
            strInfo1 = str(info).replace('(', "").replace("\'", "").replace(')', "").replace(",","")
            if int(strInfo1) == 0:
                sqlStr = "select question from question"
                cursor.execute(sqlStr)  # 执行数据库语句
                info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
                strInfo = str(info).replace('(', "").replace("\'", "").replace(')', "")
                questionItem = strInfo.split(",")
                questionList = [i for i in questionItem if i != '']
                for i in range(len(questionList)):
                    if i != 0:
                        questionList[i] = questionList[i][1:len(questionList[i])]
                return render_template('/iden/i2.html', question=questionList)
            elif int(strInfo1) == 1:
                print(session.get('user_id'))
                flash("您已经是鉴定师了！")
                return redirect(url_for('toIdentify'))
            else :
                flash("请登录后操作")
                return redirect(url_for('toIdentify'))
        else:
            return render_template('/iden/i2.html')


def i2Submit(app):
    @app.route('/i2.html/submit', methods=['POST', 'GET'])
    def submit():
        if request.method == 'POST':
            answer = request.form.to_dict()  # 获取表单内容
            sqlStr = "select answer from question where question_id=1"
            cursor.execute(sqlStr)  # 执行数据库语句
            info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
            strInfo = str(info).replace('(', "").replace("\'", "").replace(')', "").replace(",", "")
            if strInfo == answer.get('answer'):
                sqlStr = "UPDATE user SET isIdentify = 1 WHERE user_id =" + "'" + session.get('user_id') + "'"
                cursor.execute(sqlStr)  # 执行数据库语句
                conn.commit()
                flash("您已成功成为鉴定师")
            else:
                print(session.get('user_id'))
                flash("成绩过低，无法成为鉴定师")
            return redirect(url_for('toIdentify'))
        else:
            return redirect(url_for('toIdentify'))
