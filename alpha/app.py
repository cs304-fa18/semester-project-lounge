from flask import (Flask, url_for, flash, render_template, request, redirect, session, jsonify)
import events, messages, family, login, donations, feedback

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
        up_events = events.getEvents(conn, 1)
        up_id = [event['ename'].replace(' ', '') for event in up_events]
        up = [(up_events[i], up_id[i]) for i in range(len(up_events))]
        past_events = events.getPastEvents(conn, 1)
        past_id = [event['ename'].replace(' ', '') for event in past_events]
        past = [(past_events[i], past_id[i]) for i in range(len(past_events))]
        return render_template('events.html', up=up, past=past, submit = 'yes')

@app.route('/events/<eid>', methods=['GET'])
def listEvent(eid):
    conn = events.getConn('c9')
    new_id = eid.split('_')
    name = new_id[0]
    date = new_id[1]
    event = events.getEvent(conn, name, date)
    past = False
    if event in events.getPastEvents(conn, 1):
        past = True
    return render_template('event.html', event = event, past=past)
    
@app.route('/moreEvent/', methods=['POST'])
def moreEvent():
    name = request.form.get('name')
    date = request.form.get('date')
    eid = str(name) + '_' + str(date)
    return redirect(url_for('listEvent', eid=eid))

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
            up_events = events.getEvents(conn, 0)
            up_id = [event['ename'].replace(' ', '') for event in up_events]
            up = [(up_events[i], up_id[i]) for i in range(len(up_events))]
            past_events = events.getPastEvents(conn, 0)
            past_id = [event['ename'].replace(' ', '') for event in past_events]
            past = [(past_events[i], past_id[i]) for i in range(len(past_events))]
            return render_template('events.html', up=up, past=past, approve = "yes")
            
@app.route('/createEvent/', methods=['GET', 'POST'])
def createEvent():
    return render_template('createEvent.html')

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
            
        return redirect(url_for('createEvent'))

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
    events.updateRSVP(conn, name, date, session['uid'])
    flash("RSVPS for event {} increased by one".format(name))
    return redirect(request.referrer)
    
@app.route('/rsvpEventAjax/', methods=['POST'])
def rsvpEventAjax():
    conn = events.getConn('c9')
    name = request.form.get('name')
    eid = name.replace(' ', '')
    date = request.form.get('date')
    events.updateRSVP(conn, name, date, session['uid'])
    rsvp = events.getRSVP(conn, name, date)
    return jsonify({'rsvp': rsvp['rsvps'], 'name': name, 'date': date, 'eid': eid})

@app.route('/findRSVPsAjax/', methods=['POST'])
def findRSVPsAjax():
    conn = events.getConn('c9')
    name = request.form.get('name')
    date = request.form.get('date')
    rsvps = events.getPeople(conn, name, date)
    str_rsvps = [rsvp['name'] for rsvp in rsvps]
    return jsonify({'rsvps': str_rsvps})

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
@app.route('/personMs/')   
def messagePerson():
    uid = session['uid']
    person = request.args.get('person')
    curs=messages.cursor('c9')
    msgs = messages.getMessages(curs, uid, person)
    return jsonify(msgs)

# Main page for donations, showing HTML form to submit donations
@app.route('/donate/')
def makeDonation():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        return render_template('donations.html')  

@app.route('/submitDonation/', methods=['POST'])
def submitDonation():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        error = False
        uname = request.form.get('username')
        item = request.form.get('item')
        description = request.form.get('description')
        
        # Check to see all inputs have been filled out
        if uname == '':
            flash("Missing input: Please input your name")
            error = True
        
        if item == None:
            flash("Missing input: Please choose an item type")
            error = True
        
        if description == '':
            flash("Missing input: Please describe your item")
            error = True
            
        if not error:
            curs = donations.cursor('c9')
            donations.submitDonation(curs, uname, item, description)
            name=donations.getName(curs,uname)
            name=name['name']
            return render_template('donationSuccess.html', name = name) 
        return render_template('donations.html')

# An admin only page for viewing donations
@app.route('/viewDonations/')
def viewDonations():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else: # Make sure user is an admin
        if session['utype']['user_type'] == 'regular':
            flash('Not accessible for regular users')
            return redirect(url_for('makeDonation'))
        else:
            curs = donations.cursor('c9')
            oldDonations = donations.getOldDonations(curs)
            newDonations = donations.getNewDonations(curs)
            return render_template('viewDonations.html', oldDonations=oldDonations, newDonations=newDonations)

# Method to mark donations as read/unread
@app.route('/markDonation/', methods=['POST'])
def markSeen():
    curs = messages.cursor('c9')
    uid = session['uid']
    did = request.form.get('did')
    seen = 0;
    if request.form.get('submit') == "Mark as read":
        seen = 1;
    donations.mark(curs, did, seen)
    return redirect(url_for('viewDonations'))

# Main page for feedback, showing HTML form to submit feedback
@app.route('/feedback/')
def giveFeedback():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        return render_template('feedback.html') 

@app.route('/submitFeedback/', methods=['POST'])
def submitFeedback():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        error = False
        uname = request.form.get('username')
        date = request.form.get('date')
        subject = request.form.get('subject')
        message = request.form.get('message')  
        
        if message == '':
            flash("Missing input: Message is required")
            error = True
        
        if date != '':
            checkdate = "".join(request.form.get('date').split("-"))
            if not checkdate.isdigit():
                error = True
                flash("Date is not numeric")
        
        if not error:
            curs = feedback.cursor('c9')
            feedback.submitFeedback(curs, uname, date, subject, message)
            flash("Thanks for the feedback! Our admins will be in touch soon to follow up if necessary.")
        return render_template('feedback.html')

@app.route('/viewFeedback/')
def viewFeedback():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else: # Make sure user is an admin
        if session['utype']['user_type'] == 'regular':
            flash('Not accessible for regular users')
            return redirect(url_for('makeDonation'))
        else:
            curs = feedback.cursor('c9')
            fback = feedback.viewFeedback(curs)
            return render_template('viewFeedback.html', feedback=fback)

@app.route('/familySearch/', methods=['POST'])
def redirect_url():
    searchterm = request.form.get('searchterm') # take in searched search term
    return redirect(url_for('getFamily', searchterm=searchterm)) # redirect to movie page with movies matching search

@app.route('/family/', defaults={'searchterm':''}) # defaults to showing all movies
@app.route('/family/<searchterm>/', methods=['GET'])
def getFamily(searchterm):
    if session['uid'] == '': # Not logged in yet
        flash("Need to log in")
        return render_template('index.html') # Go to a temporary login 
    else:
        conn = family.getConn("c9")
        families = family.getFamily(conn, searchterm)
        names_all = [fam['name'] for fam in families]
        names = list(set(names_all))
        return render_template('family.html', families=families, names=names)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8080)