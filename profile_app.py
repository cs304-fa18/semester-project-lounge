from flask import (Flask, render_template, make_response, request,
                   redirect, url_for,
                   session, flash, send_from_directory, Response)
from werkzeug import secure_filename
app = Flask(__name__)

import sys, os, random
import imghdr
import MySQLdb
import pic_db

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

app.config['UPLOADS'] = 'uploads'

def getConn(db):
    conn = MySQLdb.connect(host='localhost',user='ubuntu',passwd='',db=db)
    conn.autocommit(True)
    return conn

@app.route('/pics/<name>')
def pic(name):
    conn = getConn('c9')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    numrows = curs.execute('select name, pic,filename from picfile inner join user on pic=username where username =%s ', [name])
    
    if numrows == 0:
        flash('No picture for {}'.format(nm))
        return redirect(url_for('index'))
    row = curs.fetchone()
    val = send_from_directory(app.config['UPLOADS'],row['filename'])
    return val

    # return render_template('all_pics.html',pics=pics)


@app.route('/upload', methods=["POST", "GET"])
def file_upload():
    if request.method =="GET":
        return render_template('picForm.html', src='',name='')
    else:
        try:
            name= request.form['id'] 
            f = request.files['pic']
            mime_type = imghdr.what(f.stream)
            if mime_type.lower() not in ['jpeg','gif','png']:
                raise Exception('Not a JPEG, GIF or PNG: {}'.format(mime_type))
            filename = secure_filename('{}.{}'.format(name,mime_type))
            pathname = os.path.join(app.config['UPLOADS'],filename)
            f.save(pathname)
            
            conn = getConn('c9')
            curs = conn.cursor()
            
            curs.execute('''update picfile set filename=%s where
                    pic=%s''', [filename, name])
            flash('Upload successful')
            return render_template('picForm.html', src=url_for('pic',name=name),
                                  name=name)
        except ZeroDivisionError as err:
            flash('Upload failed {why}'.format(why=err))
            return render_template('picForm.html', src=url_for('pic',name=name),
                                  name=name)
                                   
    
            
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)
