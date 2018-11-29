# Riann Tang

from flask import (Flask, url_for, flash, render_template, request, redirect, session, jsonify)
import messages

app = Flask(__name__)
app.secret_key = "notverysecret"
    
@app.route('/setUID/', methods=['POST'])
def setUID():
    uid = request.form.get('uid')
    if uid == '':
        session['uid'] = uid
        return redirect(request.referrer)
    session['uid'] = uid
    return redirect(request.referrer)
    
@app.route('/messages/')
def messaging():
    if session['uid'] == '': # Not logged in yet
        return render_template('empty.html')
    else:
        uid = session['uid']
        curs = messages.cursor('c9')
        allMsgs = messages.getMessageHistory(curs, uid)
        allK = list(allMsgs.keys())
        mPreview=[]
        for i in range(0,len(allK)):
            mPreview.append(messages.getLastM(curs,uid, allK[i]))
        return render_template('messages.html', msgs=allMsgs, mKeys=allK, mPrev=mPreview)
        
@app.route('/sendMsg/', methods=['POST'])
def sendMsg():
    curs = messages.cursor('c9')
    uid = session['uid']
    receiver = request.form.get('receiver')
    content = request.form.get('message')
    messages.sendMessage(curs, uid, receiver, content)
    return redirect(request.referrer)

@app.route('/sendMsgAjax/', methods=['POST'])
def sendMsgAjax():
    curs = messages.cursor('c9')
    uid = session['uid']
    receiver = request.form.get('receiver')
    content = request.form.get('message')
    messages.sendMessage(curs, uid, receiver, content)
    return jsonify(uid) #Could even return text

@app.route('/person/')   
def messagePerson():
    uid = session['uid']
    person = request.args.get('person')
    curs=messages.cursor('c9')
    msgs = messages.getMessages(curs, uid, person)
    msgsList = []
    # for i in range (0,len(msgs)):
    #     msgsList.append(msgs[i]['message'])
    return jsonify(msgs)
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)