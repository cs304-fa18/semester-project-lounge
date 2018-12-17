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

@app.route('/pics/')
def pics():
    conn = getConn('c9')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select name, pic,filename from picfile inner ')
    pics = curs.fetchall()
    return render_template('all_pics.html',pics=pics)


@app.route('/upload', methods=["POST", "GET"])
def file_upload():
    if request.method =="GET":
        return render_template('picForm.html')
    else:
        try:
            name= request.form['id'] 
            f = request.files['file']
            mime_type = imghdr.what(f.stream)
            if mime_type.lower() not in ['jpeg','gif','png']:
                raise Exception('Not a JPEG, GIF or PNG: {}'.format(mime_type))
            filename = secure_filename('{}.{}'.format(name,mime_type))
            pathname = os.path.join(app.config['UPLOADS'],filename)
            f.save(pathname)
            flash('Upload successful')
            conn = getConn('c9')
            curs = conn.cursor()
            
            curs.execute('''update picfile filename=%s where
                    pic=%s''', [name, filename])
            return render_template('picForm.html')
        except ZeroDivisionError as err:
            flash('Upload failed {why}'.format(why=err))
            return render_template('picForm.html')
    
    
            
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8083)
