from flask import (Flask, url_for, flash, render_template, request, redirect, session, jsonify)
import events, messages, family, login, donations, feedback, conn

app = Flask(__name__)
app.secret_key = "notverysecret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def adminBoard():
    if session['utype']['user_type'] == 'regular':
        flash("Only admins can view this page")
        return redirect(request.referrer)
    else:
        return render_template('admin.html')
        
@app.route('/createAccount/', methods=['GET', 'POST'])
def newAccount():
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
            curs = conn.getConn("c9")
            if login.findUser(curs, uname) is None:
                flash("{} created an account".format(uname))
                login.insertUser(curs, name, email, uname, pwd1, nname, phnum, year, sprefs)
                
                if industry != '':
                    login.insertIndustry(curs, uname, industry)
                if fname != '':
                    login.insertFamily(curs, uname, fname, ances)
                if team != '':
                    login.insertTeam(curs, uname, team, ttype, ncity, state, country)
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
    
    curs = conn.getConn("c9")
    session['utype'] = login.getUserType(curs, uid)
    return redirect(request.referrer)
    
@app.route('/approved/')
def viewApproved():
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        curs = conn.getConn('c9')
        up_events = events.getEvents(curs, 1)
        up_id = [event['ename'].replace(' ', '') for event in up_events]
        up = [(up_events[i], up_id[i]) for i in range(len(up_events))]
        past_events = events.getPastEvents(curs, 1)
        past_id = [event['ename'].replace(' ', '') for event in past_events]
        past = [(past_events[i], past_id[i]) for i in range(len(past_events))]
        return render_template('events.html', up=up, past=past, submit = 'yes')

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
            curs = conn.getConn('c9')
            all_events = events.getPastEvents(curs, 0)
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
            curs = conn.getConn('c9')
            if events.checkEvent(curs, name, date):
                flash("Event {} at {} exists".format(name, date))
            else:
                events.submitEvent(curs, name, city, state, country, desc, date, session['uid'])
                flash("Event {} submitted for approval by admins".format(name))
            
        return redirect(url_for('viewApproved'))

@app.route('/approveDeleteEvent/', methods=['POST'])
def approveDeleteEvent():
    curs = conn.getConn('c9')
    name = request.form.get('name')
    date = request.form.get('date')
    
    if request.form.get('submit') == 'Approve!':
        events.approveEvent(curs, name, date)
        flash("Event {} approved".format(name))
        return redirect(url_for('viewApproved'))
        
    if request.form.get('submit') == 'Delete!':
        print(name, date)
        events.deleteEvent(curs, name, date)
        flash("Event {} deleted".format(name))
        return redirect(url_for('viewSubmitted'))
        
@app.route('/rsvpEvent/', methods=['POST'])
def rsvpEvent():
    curs = conn.getConn('c9')
    name = request.form.get('name')
    date = request.form.get('date')
    events.updateRSVP(curs, name, date)
    flash("RSVPS for event {} increased by one".format(name))
    return redirect(request.referrer)
    
@app.route('/rsvpEventAjax/', methods=['POST'])
def rsvpEventAjax():
    curs = conn.getConn('c9')
    name = request.form.get('name')
    eid = name.replace(' ', '')
    date = request.form.get('date')
    events.updateRSVP(curs, name, date)
    rsvp = events.getRSVP(curs, name, date)
    return jsonify({'rsvp': rsvp['rsvps'], 'name': name, 'date': date, 'eid': eid})

@app.route('/messages/')
def messaging():
    """Returns html page with necessary data to populate messaging page."""
    if session['uid'] == '': # Not logged in yet
        flash("Need to log in")
        return render_template('index.html') # Go to a temporary login 
    else:
        uid = session['uid']
        curs = conn.getConn('c9')
        allMsgs = messages.getMessageHistory(curs, uid) # Get people user has messaged/received messages from
        allK = list(allMsgs.keys())
        mPreview = [messages.getLastM(curs,uid, allK[i]) for i in range(0,len(allK))]
        num = [i for i in range(0,len(allMsgs))]
        return render_template('messages.html', num=num, msgs=allMsgs, mKeys=allK, mPrev=mPreview)

@app.route('/sendMsg/', methods=['POST'])
def sendMsg():
    """Sends a new message by inserting into the messaging table"""
    curs = conn.getConn('c9')
    uid = session['uid']
    receiver = request.form.get('receiver')
    content = request.form.get('message')
    messages.sendMessage(curs, uid, receiver, content)
    return redirect(request.referrer)

# Sends new message with Ajax
@app.route('/sendMsgAjax/', methods=['POST'])
def sendMsgAjax():
    """Sends a message using Ajax updating"""
    curs = conn.getConn('c9')
    uid = session['uid']
    receiver = request.form.get('receiver')
    content = request.form.get('message')
    messages.sendMessage(curs, uid, receiver, content)
    return jsonify(uid) #Could even return text

@app.route('/personMs/')   
def messagePerson():
    """Returns all messages with a specific person"""
    uid = session['uid']
    person = request.args.get('person')
    curs = conn.getConn('c9')
    msgs = messages.getMessages(curs, uid, person)
    return jsonify(msgs)

@app.route('/donate/')
def makeDonation():
    """Returns html page populated with donation form"""
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        return render_template('donations.html')  

@app.route('/submitDonation/', methods=['POST'])
def submitDonation():
    """Submits donation by inserting the data into the donation table"""
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
            curs = conn.getConn('c9')
            donations.submitDonation(curs, uname, item, description)
            name=donations.getName(curs,uname)
            name=name['name']
            return render_template('donationSuccess.html', name = name) 
        return render_template('donations.html')

@app.route('/viewDonations/')
def viewDonations():
    """Returns html page populated with data of all submitted donations"""
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else: # Make sure user is an admin
        if session['utype']['user_type'] == 'regular':
            flash('Not accessible for regular users')
            return redirect(url_for('makeDonation'))
        else:
            curs = conn.getConn('c9')
            oldDonations = donations.getOldDonations(curs)
            newDonations = donations.getNewDonations(curs)
            return render_template('viewDonations.html', oldDonations=oldDonations, newDonations=newDonations)

@app.route('/markDonation/', methods=['POST'])
def markSeen():
    """Mark all messages as seen or unseen by updating the seen column of the donation table."""
    curs = conn.getConn('c9')
    uid = session['uid']
    did = request.form.get('did')
    seen = 0;
    if request.form.get('submit') == "Mark as read":
        seen = 1;
    donations.mark(curs, did, seen)
    return redirect(url_for('viewDonations'))

@app.route('/feedback/')
def giveFeedback():
    """Return html page with feedback form"""
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else:
        return render_template('feedback.html') 

@app.route('/submitFeedback/', methods=['POST'])
def submitFeedback():
    """Submit feedback by inserting feedback data into feedback table."""
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
       
        if uname == "": # PID in table must be specified or assigned NULL
            uname = None
            
        if not error:
            curs = conn.getConn('c9')
            feedback.submitFeedback(curs, uname, date, subject, message)
            flash("Thanks for the feedback! Our admins will be in touch soon to follow up if necessary.")
        return render_template('feedback.html')

@app.route('/viewFeedback/')
def viewFeedback():
    """Return all submitted feedback in html page"""
    if session['uid'] == '':
        flash("Need to log in")
        return redirect(request.referrer)
    else: # Make sure user is an admin
        if session['utype']['user_type'] == 'regular':
            flash('Not accessible for regular users')
            return redirect(url_for('makeDonation'))
        else:
            curs = conn.getConn('c9')
            fback = feedback.viewFeedback(curs)
            return render_template('viewFeedback.html', feedback=fback)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8080)