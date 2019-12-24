from flask import request, render_template, session, make_response, flash, redirect, url_for
from pymysql import *
from werkzeug.security import check_password_hash

conn = connect(host='localhost', port=3306, user='root', passwd='123', db='tjh', charset='utf8')
cursor = conn.cursor()


def quickView(app):
    @app.route('/qv.html', methods=['POST', 'GET'])
    def result():
        if request.method == 'GET':
            return render_template('/info/qv.html')
        else:
            return render_template('/info/qv.html')
