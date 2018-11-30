from flask import (Flask, url_for, flash, render_template, request, redirect, session, jsonify)
import events, messages

app = Flask(__name__)
app.secret_key = "notverysecret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/approved/')
def viewApproved():
    conn = events.getConn('c9')
    all_events = events.getEvents(conn, 1)
    return render_template('events.html', events=all_events)

@app.route('/submitted/')
def viewSubmitted():
    conn = events.getConn('c9')
    all_events = events.getEvents(conn, 0)
    return render_template('events.html', events=all_events, approve = "yes")

@app.route('/submitEvent/', methods=['POST'])
def submitEvent():
    error = False
    name = ''
    city = ''
    state = ''
    country = ''
    description = ''
    date = ''
    
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        desc = request.form.get('desc')
        date = request.form.get('date')
    except:
        flash("Access to missing form inputs")
        error = True
    
    if name == '':
        flash("Missing input: Event's name is missing")
        error = True
    
    checkdate = "".join(request.form.get('date').split("-"))
    if not checkdate or not checkdate.isdigit():
        error = True
        if not checkdate:
            flash("Missing input: Event's date is missing")
        else:
            flash("Date is not numeric")
    
    if not error:
        conn = events.getConn('c9')
        if events.checkEvent(conn, name, date):
            flash("Event {} at {} exists".format(name, date))
        else:
            events.submitEvent(conn, name, city, state, country, desc, date)
            flash("Event {} submitted for approval by admins".format(name))
            
    return redirect(url_for('viewApproved'))

@app.route('/approveDeleteEvent/', methods=['POST'])
def approveDeleteEvent():
    conn = events.getConn('c9')
    name = request.form.get('name')
    date = request.form.get('date')
    if request.form.get('submit') == 'Approve!':
        events.approveEvent(conn, name, date)
        flash("Event {} approved".format(name))
        return redirect(url_for('viewApproved'))
    if request.form.get('submit') == 'Delete this!':
        print(name, date)
        flash("Event {} deleted".format(name))
        flash("Event {} deleted".format(name))
        return redirect(url_for('viewSubmitted'))
    
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
    app.run('0.0.0.0',8080)