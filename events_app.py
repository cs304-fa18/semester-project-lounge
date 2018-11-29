# Lauren Tso 
from flask import (Flask, url_for, flash, render_template, request, redirect, session, jsonify)
import events

app = Flask(__name__)
app.secret_key = "notverysecret"

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

@app.route('/approveEvent/', methods=['POST'])
def approveEvent():
    conn = events.getConn('c9')
    name = request.form.get('name')
    date = request.form.get('date')
    events.approveEvent(conn, name, date)
    flash("Event {} approved".format(name))
    return redirect(url_for('viewApproved'))

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8080)
