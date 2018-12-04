from flask import (Flask, url_for, flash, render_template, request, redirect, session, jsonify)
import events, messages, login, family

app = Flask(__name__)
app.secret_key = "notverysecret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createAccount/', methods=['GET', 'POST'])
def logins():
    if request.method == 'GET':
        return render_template('userinfo.html')
    if request.method == 'POST':
        error = False
        email = ''
        uname = ''
        pwd1 = ''
        pwd2 = ''
        name = ''
        nname = ''
        year = ''
        phnum = ''
        sprefs = ''
        industry = ''
        fname = ''
        ances = ''
        team = ''
        ttype = ''
        ncity= ''
        state = ''
        country = ''
        
        try:
            email = request.form.get("email")
            uname = request.form.get("username")
            pwd1 = request.form.get("password1")
            pwd2 = request.form.get("password2")
            name = request.form.get("name")
            nname = request.form.get("nickname")
            year = request.form.get("year")
            phnum = request.form.get("phnum")
            sprefs = request.form.get("sprefs")
            industry = request.form.get("ind")
            fname = request.form.get("fname")
            ances = request.form.get("ancestor")
            team = request.form.get("team")
            ttype = request.form.get("t")
            ncity = request.form.get("tcity")
            state = request.form.get("tstate")
            country = request.form.get("tcountry")
        except:
            flash("Access to missing form inputs")
            error = True
        
        if uname == '':
            error = True
            flash("Missing input: Username is missing")
        if pwd1 == '' or pwd2 == '':
            error = True
            flash("Missing input: One or both of the password fields are incomplete")
        if pwd1 != pwd2:
            error = True
            flash("Passwords do not match")    
        if email == '' or "@" not in email:
            error = True
            flash("Invalid email address")
        if name == '':
            error = True
            flash("Missing input: Name is missing")
        if not year.isdigit():
            error = True
            flash("Invalid class year")
        if sprefs == '':
            error = True
            flash("Missing input: Security preferences missing")
        
        if not error:
            conn = login.getConn("c9")
            if login.findUser(conn, uname) is None:
                flash("{} created an account".format(uname))
                login.insertUser(conn, name, email, uname, pwd1, nname, phnum, year, sprefs)
                
                if industry != '':
                    login.insertIndustry(conn, uname, industry)
                if fname != '':
                    login.insertFamily(conn, uname, fname, ances)
                if team != '':
                    login.insertTeam(conn, uname, team, ttype, ncity, state, country)
                return redirect(url_for('index'))
            else:
                flash("Username already exists") # username not in database
                return redirect(request.referrer)
        else:
            return redirect(request.referrer)
                
# Sets the user of the session
@app.route('/setUID/', methods=['POST'])
def setUID():
    uid = request.form.get('uid')
    session['uid'] = uid
    
    conn = login.getConn("c9")
    session['utype'] = login.getUserType(conn, uid)
    return redirect(request.referrer)
    
@app.route('/approved/')
def viewApproved():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        conn = events.getConn('c9')
        all_events = events.getEvents(conn, 1)
        return render_template('events.html', events=all_events, submit = 'yes')

@app.route('/submitted/')
def viewSubmitted():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        if session['utype']['user_type'] == 'regular':
            flash('Not accessible for regular users')
            return redirect(url_for('viewApproved'))
        else:
            conn = events.getConn('c9')
            all_events = events.getEvents(conn, 0)
            return render_template('events.html', events=all_events, approve = "yes")

@app.route('/submitEvent/', methods=['POST'])
def submitEvent():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        error = False
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        desc = request.form.get('desc')
        date = request.form.get('date')
        
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
                events.submitEvent(conn, name, city, state, country, desc, date, session['uid'])
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
        
    if request.form.get('submit') == 'Delete!':
        print(name, date)
        events.deleteEvent(conn, name, date)
        flash("Event {} deleted".format(name))
        return redirect(url_for('viewSubmitted'))
        
@app.route('/rsvpEvent/', methods=['POST'])
def rsvpEvent():
    conn = events.getConn('c9')
    name = request.form.get('name')
    date = request.form.get('date')
    events.updateRSVP(conn, name, date)
    flash("RSVPS for event {} increased by one".format(name))
    return redirect(request.referrer)
    
@app.route('/rsvpEventAjax/', methods=['POST'])
def rsvpEventAjax():
    conn = events.getConn('c9')
    name = request.form.get('name')
    date = request.form.get('date')
    events.updateRSVP(conn, name, date)
    rsvp = events.getRSVP(conn, name, date)
    print(rsvp)
    return jsonify({'rsvp': rsvp['rsvps'], 'name': name, 'date': date})

# Main page for messaging feature    
@app.route('/messages/')
def messaging():
    if session['uid'] == '': # Not logged in yet
        flash("Need to log in")
        return render_template('index.html') # Go to a temporary login 
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

@app.route('/family/', methods=['GET'])
def families():
    if session['uid'] == '': # Not logged in yet
        flash("Need to log in")
        return render_template('index.html') # Go to a temporary login 
    else:
        conn = family.getConn("c9")
        families = family.getAll(conn)
        names_all = [fam['name'] for fam in families]
        names = list(set(names_all))
        return render_template('family.html', families=families, names=names)

# @app.route('familySearch', methods=['POST'])
# def familySearch():
#     return render_template()

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8080)