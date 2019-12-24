import random
import re
import flask_mail as flaskmail
from werkzeug.security import generate_password_hash
from threading import Thread
from flask import current_app
from datetime import datetime
from flask import request, render_template, session, make_response, flash, redirect, url_for, jsonify
import redis
from pymysql import *

conn = connect(host='localhost', port=3306, user='root', passwd='123', db='tjh', charset='utf8')
cursor = conn.cursor()

def register(app,mail,redis_store):

    @app.route('/register.html', methods=['POST', 'GET'])
    def register():
        if request.method == 'POST':
            try:
                email = request.form.get("form-email")
                code = request.form.get("form-code")
                username = request.form.get("form-username")
                password = request.form.get('form-password')
                password_again = request.form.get('form-password-again')
                mailcode_server = redis_store.get('EMAILCODE:' + email).decode()
            except Exception as e:
                current_app.logger.debug(e)
                return jsonify(re_code="1", msg='查询邮箱验证码失败')

            # 判断id有没有被注册
            strsql = "select * from user where user_id=" + username
            cursor.execute(strsql);
            count = cursor.fetchall().count();
            app.logger.debug(count)
            if (count == 0):
                if (code == mailcode_server):
                    if (password == password_again):
                        password_hash = generate_password_hash(password)
                        sqlstr = "insert into user values('%s','%s','%s')" % (username, password_hash, email)
                        cursor.execute(sqlstr)
                        conn.commit()
                        flash("注册成功")
                        return redirect(url_for('toLogin'))
                    else:
                        flash("两次密码")
                else:
                    flash("验证码错误！")
        return render_template('register.html')

    @app.route('/register/sendmail', methods=['POST'])
    def sendmail():
        email = request.form.get('email')

        if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
            return jsonify(re_code="1", msg='请填写正确的邮箱')

        # 生成邮箱验证码
        email_code = '%06d' % random.randint(0, 99999)
        app.logger.debug('邮箱验证码为: ' + email_code)
        try:
            redis_store.set('EMAILCODE:' + email, email_code, 1800)  # half-hour = 1800有效期
        except Exception as e:
            app.logger.debug(e)
            return jsonify(re_code="2", msg='存储邮箱验证码失败')
        # 发送邮件
        send_mail(
            to=email,
            mailcode=email_code
        )
        return jsonify(re_code='OK', msg='验证码发送成功')


    def send_async_email(app, msg):
        with app.app_context():   # 确认程序上下文被激活
            mail.send(msg)


    def send_mail(to, mailcode):
        app = current_app._get_current_object()
        msg = flaskmail.Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + "您的账号注册验证码",
                      sender=app.config['FLASK_MAIL_SENDER'],
                      recipients=[to])
        # 邮件内容会以文本和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
        msg.body = 'sended by flask-email'
        msg.html = '''
        <h1>
            亲爱的,
        </h1>
        <h3>
            欢迎来到 <b>球鞋资讯平台</b>!
        </h3>
        <p>
            您的验证码为 &nbsp;&nbsp; <b>{mailcode}</b> &nbsp;&nbsp; 赶快去完善注册信息吧！！！
        </p>

        <p>感谢您的支持和理解</p>
        <p>来自：Flask-Test-Project</p>
        <p><small>{time}</small></p>
        '''.format(mailcode=mailcode, time=datetime.utcnow)
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
        return thread

    return "register"
