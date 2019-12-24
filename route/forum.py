from flask import render_template, session, flash, request, redirect, url_for
from datetime import datetime
from pymysql import connect

conn = connect(host='localhost', port=3306, user='root', passwd='123', db='tjh', charset='utf8')
cursor = conn.cursor()

def forum(app):
    @app.route('/forum.html')
    def toForum():
        strsql='''select invitation.*,count(ExtraInvitation_id) from invitation left 
                join extrainvitation on invitation_id=InvitationId
                group by invitation_id
                order by invitation_date;'''
        cursor.execute(strsql)
        items=cursor.fetchall()
        return render_template('forum/forum.html', items=items)

    @app.route('/forum/<int:id>',methods=["POST","GET"])
    def toPost(id):
        app.logger.debug(session)
        strsql='update invitation set number_point=number_point+1 where invitation_id='+str(id)
        cursor.execute(strsql)
        conn.commit()
        app.logger.debug('点击数+1')
        strsql='select * from invitation where invitation_id='+str(id)
        cursor.execute(strsql)
        info=cursor.fetchall()
        strsql='select * from extrainvitation where InvitationId='+str(id)+" order by Extrainvitation_date"
        cursor.execute(strsql)
        items=cursor.fetchall()
        if(request.method=='POST'):
            if(session.get('user_id') is not None):
                username=session.get('user_id')
                replytext=request.form.get('add-forum-replytext')
                date = str(datetime.now()).split('.')[0]

                if(len(replytext)==0):
                    flash("回复内容不能为空")
                    return render_template('forum/forumpost.html', info=info[0], items=items)
                strsql="insert into extrainvitation(ExtraInvitation_text,posterId,InvitationId,ExtraInvitation_date)"\
                        "values ('%s','%s','%s','%s')" %(replytext,username,str(id),date)
                cursor.execute(strsql)
                conn.commit()
                return redirect(url_for('toPost',id=id))
            flash("你还没有登入")
        return render_template('forum/forumpost.html', info=info[0], items=items)

    @app.route('/forum/add',methods=['POST','GET'])
    def addPost():
        if request.method=='POST':
            if session.get('user_id') is not None:
                userid=session.get('user_id')
                context=request.form.get('add-forum-text')
                title=request.form.get('add-forum-title')
                date=str(datetime.now()).split('.')[0]
                if(len(title)==0 or len(context)==0):
                    flash("标题或内容不能为空")
                    return render_template('forum/addpost.html')
                strsql="insert into invitation(invitation_name,invitation_text,posterId,invitation_date) " \
                       "values('%s','%s','%s','%s')" % (title, context, userid, date)
                #print(strsql)
                cursor.execute(strsql)
                conn.commit()
                return redirect(url_for('toForum'))
            else:
                flash("没登录呢？你想干啥？")
        return render_template('forum/addpost.html')


    # @app.route('/forum/del',methods=['POST'])
    # def delPost():
    #     if session.get('user_id') is not None:
    #         userid = session.get('user_id');
    #
    #         strsql = 'select '
    #     else:
    #         flash("没登录呢？你想干啥？")
    #     pass