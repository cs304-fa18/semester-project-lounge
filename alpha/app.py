from flask import (Flask, url_for, flash, render_template, request, redirect, session, jsonify)
from datetime import date, datetime
from threading import Thread, Lock
import events, messages, family, login, donations, feedback, conn, profiles, search
from werkzeug import secure_filename
import bcrypt

app = Flask(__name__)
app.secret_key = "notverysecret"
lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/')
def adminBoard():
    if session.get('uid') == None:
        flash("Need to log in")
        return redirect(url_for('index'))
    if session.get('utype') == 'regular':
        flash('Need admin privileges')
        return redirect(url_for('index'))
    else:
        return render_template('admin.html')

@app.route('/account/', methods=['GET', 'POST'])
def account():
    return render_template('userinfo.html')

@app.route('/createAccount/', methods=['GET', 'POST'])
def newAccount():
    if request.method == 'GET':
        return redirect(url_for('account'))
    if request.method == 'POST':
        error = False
        email = request.form.get("email", '')
        uname = request.form.get("username", '')
        pwd1 = request.form.get("password1", '')
        pwd2 = request.form.get("password2", '')
        sprefs = request.form.get("sprefs", '')

        if uname == '':
            error = True
            flash("Missing input: Username is missing")
        if pwd1 == '' or pwd2 == '':
            error = True
            flash("Missing input: One or both of the password fields are incomplete")
        if pwd1 != pwd2:
            error = True
            flash("Passwords do not match")    
        if "@" not in email:
            error = True
            flash("Invalid email address")
        if sprefs == '':
            error = True
            flash("Missing input: Security preferences missing")
        
        if error:
             return redirect(request.referrer)

        curs = conn.getConn()
        hashed = bcrypt.hashpw(pwd1.encode('utf-8'), bcrypt.gensalt())
        print('hased is ' + hashed)
        if login.findUser(curs, uname) is not None:
            flash('That username is taken')
            return redirect(url_for('index'))
        login.insertUser(curs, email, uname, hashed, sprefs)
        return redirect(url_for('index'))
            
@app.route('/login/', methods=['POST'])
def loginuser():
    try:
        username = request.form.get('uid')
        passwd = request.form.get('pwd')
        curs = conn.getConn()
        row = login.getPassword(curs, username)
        if row is None:
            # Same response as wrong password, so no information about what went wrong
            flash('login incorrect. Try again or join')
            return redirect( url_for('index'))
        hashed = row['password']
        utype = row['user_type']
        # strings always come out of the database as unicode objects
        if bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8')) == hashed:
            flash('successfully logged in as '+ username)
            session['username'] = username
            session['logged_in'] = True
            session['visits'] = 1
            session['utype'] = utype
            return redirect(url_for('index'))
        else:
            flash('login incorrect. Try again or join')
            return redirect(url_for('index'))
    except Exception as err:
        flash('form submission error '+ str(err))
        return redirect( url_for('index') )

@app.route('/logout/', methods=['POST'])
def logout():
    try:
        if 'username' in session:
            username = session['username']
            session.pop('username')
            session.pop('logged_in')
            flash('{} is logged out'.format(username))
            return redirect(url_for('index'))
        else:
            flash('you are not logged in. Please login or join')
            return redirect( url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )

@app.route('/completeProfile/', methods=['GET', 'POST'])
def completeProfile():
    return render_template('moreinfo.html')

@app.route('/updateProfile/', methods=['POST'])
def updateProfile():
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
    else:
        uname = session.get('uid')
        name = request.form.get("name", '')
        nname = request.form.get("nickname", '')
        year = request.form.get("year", '')
        phnum = request.form.get("phnum", '')
        industry = request.form.get("ind", '')
        fname = request.form.get("fname", '')
        ances = request.form.get("ancestor", '')
        team = request.form.get("team", '')
        ttype = request.form.get("t", '')
        ncity = request.form.get("tcity", '')
        state = request.form.get("tstate", '')
        country = request.form.get("tcountry", '')
        
        error = False
        if name == '':
            error = True
            flash("Missing input: Name is missing")
        if not year.isdigit():
            error = True
            flash("Invalid class year")
        
        if not error:
            curs = conn.getConn()
            login.updateUser(curs, uname, name, nname, phnum, year)
                    
            if industry != '':
                login.insertIndustry(curs, uname, industry)
            if fname != '':
                login.insertFamily(curs, uname, fname, ances)
            if team != '':
                login.insertTeam(curs, uname, team, ttype, ncity, state, country)
            flash('updated profile!')
            return redirect(url_for('index'))
        else:
            return redirect(request.referrer)

@app.route('/approved/')
def viewApproved():
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
    else:
        curs = conn.getConn()
        up_events = events.getEvents(curs, 1)
        up_id = [event['ename'].replace(' ', '') for event in up_events]
        up = [(up_events[i], up_id[i]) for i in range(len(up_events))]
        past_events = events.getPastEvents(curs, 1)
        past_id = [event['ename'].replace(' ', '') for event in past_events]
        past = [(past_events[i], past_id[i]) for i in range(len(past_events))]
        return render_template('events.html', up=up, past=past, submit = 'yes')

@app.route('/events/<eid>', methods=['GET'])
def listEvent(eid):
    curs = conn.getConn()
    new_id = eid.split('_')
    name = new_id[0]
    date = new_id[1]
    event = events.getEvent(curs, name, date)
    past = False
    approved = False
    if event in events.getPastEvents(curs, 1):
        past = True
    if event in events.getEvents(curs, 1):
        approved = True
    return render_template('event.html', event = event, past=past, approved=approved)
    
@app.route('/moreEvent/', methods=['POST'])
def moreEvent():
    name = request.form.get('name')
    date = request.form.get('date')
    eid = str(name) + '_' + str(date)
    return redirect(url_for('listEvent', eid=eid))

@app.route('/submitted/')
def viewSubmitted():
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
    else:
        if session.get('utype') == 'regular':
            flash('Not accessible for regular users')
            return redirect(url_for('viewApproved'))
        else:
            curs = conn.getConn()
            up_events = events.getEvents(curs, 0)
            up_id = [event['ename'].replace(' ', '') for event in up_events]
            up = [(up_events[i], up_id[i]) for i in range(len(up_events))]
            past_events = events.getPastEvents(curs, 0)
            past_id = [event['ename'].replace(' ', '') for event in past_events]
            past = [(past_events[i], past_id[i]) for i in range(len(past_events))]
            return render_template('events.html', up=up, past=past, approve = "yes")
            
@app.route('/createEvent/', methods=['GET', 'POST'])
def createEvent():
    return render_template('createEvent.html')

@app.route('/submitEvent/', methods=['POST'])
def submitEvent():
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
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

        if not date or type(date) is not datetime.date:
            error = True
            if not date:
                flash("Missing input: Event's date is missing")
            else:
                flash("Date is not numeric")
        
        if not error:
            curs = conn.getConn()
            lock.acquire()
            if events.checkEvent(curs, name, date):
                flash("Event {} at {} exists".format(name, date))
            else:
                events.submitEvent(curs, name, city, state, country, desc, date, session['uid'])
                flash("Event {} submitted for approval by admins".format(name))
            lock.release()
        return redirect(url_for('createEvent'))

@app.route('/approveDeleteEvent/', methods=['POST'])
def approveDeleteEvent():
    curs = conn.getConn()
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
    curs = conn.getConn()
    name = request.form.get('name')
    date = request.form.get('date')
    events.updateRSVP(curs, name, date, session['uid'])
    flash("RSVPS for event {} increased by one".format(name))
    return redirect(request.referrer)
    
@app.route('/rsvpEventAjax/', methods=['POST'])
def rsvpEventAjax():
    curs = conn.getConn()
    name = request.form.get('name')
    eid = name.replace(' ', '')
    date = request.form.get('date')
    events.updateRSVP(curs, name, date, session['uid'])
    rsvp = events.getRSVP(curs, name, date)
    return jsonify({'rsvp': rsvp['rsvps'], 'name': name, 'date': date, 'eid': eid})

@app.route('/findRSVPsAjax/', methods=['POST'])
def findRSVPsAjax():
    curs = conn.getConn()
    name = request.form.get('name')
    date = request.form.get('date')
    rsvps = events.getPeople(curs, name, date)
    str_rsvps = [rsvp['name'] for rsvp in rsvps]
    return jsonify({'rsvps': str_rsvps})

@app.route('/messages/')
def messaging():
    """Returns html page with necessary data to populate messaging page."""
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
    else:
        uid = session['uid']
        curs = conn.getConn()
        allMsgs = messages.getMessageHistory(curs, uid) # Get people user has messaged/received messages from
        allK = list(allMsgs.keys())
        mPreview = [messages.getLastM(curs,uid, allK[i]) for i in range(0,len(allK))]
        num = [i for i in range(0,len(allMsgs))]
        return render_template('messages.html', num=num, msgs=allMsgs, mKeys=allK, mPrev=mPreview)

@app.route('/sendMsg/', methods=['POST'])
def sendMsg():
    """Sends a new message by inserting into the messaging table"""
    curs = conn.getConn()
    uid = session['uid']
    receiver = request.form.get('receiver')
    content = request.form.get('message')
    messages.sendMessage(curs, uid, receiver, content)
    return redirect(request.referrer)

# Sends new message with Ajax
@app.route('/sendMsgAjax/', methods=['POST'])
def sendMsgAjax():
    """Sends a message using Ajax updating"""
    curs = conn.getConn()
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
    curs = conn.getConn()
    msgs = messages.getMessages(curs, uid, person)
    return jsonify(msgs)

@app.route('/donate/')
def makeDonation():
    """Returns html page populated with donation form"""
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
    else:
        return render_template('donations.html')  

@app.route('/submitDonation/', methods=['POST'])
def submitDonation():
    """Submits donation by inserting the data into the donation table"""
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
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
            curs = conn.getConn()
            donations.submitDonation(curs, uname, item, description)
            name=donations.getName(curs,uname)
            name=name['name']
            return render_template('donationSuccess.html', name = name) 
        return render_template('donations.html')

@app.route('/viewDonations/')
def viewDonations():
    """Returns html page populated with data of all submitted donations"""
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
    else: 
        if session.get('utype') == 'regular': # Make sure user is an admin
            flash('Not accessible for regular users')
            return redirect(url_for('makeDonation'))
        else:
            curs = conn.getConn()
            oldDonations = donations.getOldDonations(curs)
            newDonations = donations.getNewDonations(curs)
            return render_template('viewDonations.html', oldDonations=oldDonations, newDonations=newDonations)

@app.route('/markDonation/', methods=['POST'])
def markSeen():
    """Mark all messages as seen or unseen by updating the seen column of the donation table."""
    curs = conn.getConn()
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
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
    else: 
        return render_template('feedback.html') 

@app.route('/submitFeedback/', methods=['POST'])
def submitFeedback():
    """Submit feedback by inserting feedback data into feedback table."""
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
        curs = conn.getConn()
        feedback.submitFeedback(curs, uname, date, subject, message)
        flash("Thanks for the feedback! Our admins will be in touch soon to follow up if necessary.")
    return render_template('feedback.html')

@app.route('/viewFeedback/')
def viewFeedback():
    """Return all submitted feedback in html page"""
    if session.get('uid') == None:
        flash("Need to log in")
        return render_template('index.html')
    else: 
        if session.get('utype') == 'regular': # Make sure user is an admin
            flash('Not accessible for regular users')
            return redirect(url_for('makeDonation'))
        else:
            curs = conn.getConn()
            fback = feedback.viewFeedback(curs)
            return render_template('viewFeedback.html', feedback=fback)

@app.route('/familySearch/', methods=['POST'])
def redirect_url():
    searchterm = request.form.get('searchterm') # take in searched search term
    return redirect(url_for('getFamily', searchterm=searchterm)) # redirect to movie page with movies matching search

@app.route('/family/', defaults={'searchterm':''}) # defaults to showing all families
@app.route('/family/<searchterm>/', methods=['GET'])
def getFamily(searchterm):
    if session.get('uid') == None:# Not logged in yet
        flash("Need to log in")
        return render_template('index.html') # Go to a temporary login 
    else:
        curs = conn.getConn()
        families = family.getFamily(curs, searchterm)
        names_all = [fam['name'] for fam in families]
        names = list(set(names_all))
        return render_template('family.html', families=families, names=names)
        
@app.route('/profile/<username>/', methods=['GET'])
def getProfile(username):
    """Retrieves the profile of the given user and ensures security preferences are respected"""
    currentU = session.get('uid')
    if currentU == None:
        flash("Need to log in")
        return render_template('index.html')
        
    curs = conn.getConn()

    # check = profiles.checkPerson(curs, username)
    # if len(check) == 0:
    #     return render_template('search.html', dne=1)

    #Get all the user's info
    basic = profiles.getBasicInfo(curs, username)
    industry = profiles.getIndustry(curs, username)
    team = profiles.getTeam(curs, username)
    contact = profiles.getContactInfo(curs, username)
    
    #Check user's security preferences and whether person viewing profiles matches prefs
    prefs = profiles.getSecurityPrefs(curs, username)['sprefs']

    if session.get('utype') == 'admin': #Admins can always view all info
        permiss =1 
    elif prefs == "all":
        permiss = 1
    elif prefs == "class":
        if profiles.getYear(curs, username) == profiles.getYear(curs, currentU):
            print "same class"
            permiss = 1
    elif prefs == "overlap":
        if profiles.getOverlap(curs, username, currentU) == 1:
            permiss = 1
    
    try: # Determine how much to show on html page
        permiss
        return render_template('profile.html', basic=basic, industry=industry, team=team, 
                                contact=contact, permiss=permiss)
    except NameError:
        npermiss = 1
        return render_template('profile.html', basic=basic, industry=industry, team=team, 
                                contact=contact, npermiss=npermiss)

@app.route("/search", methods=["GET", "POST"])
def searchPerson():
    if session.get('uid') == None:# Not logged in yet
        flash("Need to log in")
        return render_template('index.html') # Go to a temporary login 
    if request.method == 'GET':
        return render_template('search.html')
    else:
        name = request.form.get("name")
        year= request.form.get("year")
        indust = request.form.get("Industry")
        
        if all([name=="", year=="", indust==""]):
            flash("enter something to filter your search by")
            return render_template('search.html')

                
        searchItems = []
        if name!="":
            searchItems.append(["name", "%"+name+"%"])
        if year !="" and year.isdigit():
            searchItems.append(["classyear","%"+year+"%" ])
        if indust !="":
            searchItems.append(["iname","%"+indust+"%" ])
        
        transpose = zip(*searchItems)
        
        curs = conn.getConn()
        table = search.search(curs, transpose)
        
        return render_template('search.html', table=table)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8080)