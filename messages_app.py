# Riann Tang

from flask import (Flask, url_for, flash, render_template, request, redirect, session, jsonify)
import messages

app = Flask(__name__)
app.secret_key = "notverysecret"

# Sets the user of the session
@app.route('/setUID/', methods=['POST'])
def setUID():
    uid = request.form.get('uid')
    if uid == '':
        session['uid'] = uid
        return redirect(request.referrer)
    session['uid'] = uid
    return redirect(request.referrer)

# Main page for messaging feature    
@app.route('/messages/')
def messaging():
    if session['uid'] == '': # Not logged in yet
        return render_template('empty.html') # Go to a temporary login 
    else:
        uid = session['uid']
        curs = messages.cursor('c9')
        allMsgs = messages.getMessageHistory(curs, uid) # Get people user has messaged/received messages from
        allK = list(allMsgs.keys())
        mPreview=[] # Empty list to store a preview of messages with each person
        num=[] # For navigating for all the inputs in html page
        for i in range(0,len(allK)):
            mPreview.append(messages.getLastM(curs,uid, allK[i]))
        for i in range(0,len(allMsgs)):
            num.append(i)
        return render_template('messages.html', num=num, msgs=allMsgs, mKeys=allK, mPrev=mPreview)

# Sends new message        
@app.route('/sendMsg/', methods=['POST'])
def sendMsg():
    curs = messages.cursor('c9')
    uid = session['uid']
    receiver = request.form.get('receiver')
    content = request.form.get('message')
    messages.sendMessage(curs, uid, receiver, content)
    return redirect(request.referrer)

# Sends new message with Ajax
@app.route('/sendMsgAjax/', methods=['POST'])
def sendMsgAjax():
    curs = messages.cursor('c9')
    uid = session['uid']
    receiver = request.form.get('receiver')
    content = request.form.get('message')
    messages.sendMessage(curs, uid, receiver, content)
    return jsonify(uid) #Could even return text

# For showing messages with an individual person
@app.route('/person/')   
def messagePerson():
    uid = session['uid']
    person = request.args.get('person')
    curs=messages.cursor('c9')
    msgs = messages.getMessages(curs, uid, person)
    return jsonify(msgs)
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)