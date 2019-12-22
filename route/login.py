from flask import request, render_template, session, make_response, flash, redirect, url_for
from pymysql import *
from werkzeug.security import check_password_hash

conn = connect(host='localhost', port=3306, user='root', passwd='123', db='tjh', charset='utf8')
cursor = conn.cursor()


def logIn(app):
    @app.route('/login', methods=['POST', 'GET'])
    def result():
        if request.method == 'POST':
            # pin = variable
            # print(pin)
            # print("是否选择记住密码checkBox:", request.form.get("remember"))
            user_info = request.form.to_dict()  # 获取表单内容
            sqlStr = "select * from user"  # 数据库操作
            cursor.execute(sqlStr)  # 执行数据库语句
            info = cursor.fetchall()  # 将获取到的数据库文件转化为字符串
            flag = 0  # 判断数据库里是否存在账号
            for item in info:
                if item[0] == user_info.get("id"):  # 验证账号是否存在数据库中
                    if check_password_hash(item[1],user_info.get("pwd")) and user_info.get("pin") == '1':  # 密码验证码匹配成功
                        resp = make_response(render_template('index.html'))
                        resp.set_cookie('user_id', user_info.get("id"))
                        flag = 1
                        print(item[0])
                        if request.form.get("remember") is None:  # 没有记住账号
                            print(222222)
                            pass
                        else:  # 记住密码
                            # 将账号保存到cookie中
                            session.permanent = True
                            session['user_id'] = user_info.get("id")
                            print(3333333)
                        return render_template('index.html')
                    else:
                        flag = 1
                        flash("账号或密码错误！")
                        return redirect(url_for('toLogin'))
            if flag == 0:
                flash("不存在该账号")
                return redirect(url_for('toLogin'))