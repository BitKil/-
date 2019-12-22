from datetime import timedelta

import redis
import flask_mail as flaskmail
from route.login import logIn
from route.register import register
from flask import Flask, request, url_for, render_template

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
    return render_template('index.html')


@app.route('/information.html')
def toInformation():
    return render_template('information.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


logIn(app)
register(app,mail,redis_store)

if __name__ == '__main__':
    app.run()
