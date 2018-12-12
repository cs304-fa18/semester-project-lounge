# Lauren Tso

import sys
import MySQLdb

# ================================================================

def getEvent(curs, name, date):
    '''returns the event matching the unique name and date given'''
    curs.execute('''select * from events where ename = %s and edate = %s''', (name, date,))
    return curs.fetchone()
                           
def getEvents(curs, approved):
    '''returns all upcoming events that are or are not approved'''
    curs.execute('''select * from events where approved = %s and edate >= current_timestamp()
                    order by edate asc''', (approved,))
    return curs.fetchall()
    
def getPastEvents(curs, approved):
    '''returns all past events that are (1) or are not approved (0)'''
    curs.execute('''select * from events where approved = %s and edate < current_timestamp()
                    order by edate asc''', (approved,))
    return curs.fetchall()
    
def checkEvent(curs, name, date):
    '''returns true if event with same name and date already exists'''
    curs.execute('''select count(*) as count from events where ename = %s and edate = %s''', (name, date,))
    row = curs.fetchone()
    return row['count'] > 0
    
def submitEvent(curs, name, city, state, country, desc, date, uname):
    '''inserts event with all accompanying data into the events table'''
    curs.execute('''insert into events(ename, city, state, country, description, edate, approved, pid) 
                    values(%s, %s, %s, %s, %s, %s, 0, %s)''', (name, city, state, country, desc, date, uname,))
                    
def approveEvent(curs, name, date):
    '''set event with given name and date as approved -- for admins'''
    curs.execute('''update events set approved = 1 where ename = %s and edate = %s''', (name, date,))

def deleteEvent(curs, name, date):
    '''delete event with given name and date -- for admins'''
    curs.execute('''delete from events where ename = %s and edate = %s''', (name, date,))

def updateRSVP(curs, name, date, uname):
    '''update rsvps for the event with the given name and date for the user'''
    curs.execute('''insert into rsvps(uname, ename, edate) values(%s, %s, %s)''', (uname, name, date,))
    curs.execute('''update events set rsvps = rsvps + 1 where ename = %s and edate = %s''', (name, date,)) # need to inner join on rsvps

def getRSVP(curs, name, date):
    '''return number of rsvps for the event with the given name and date'''
    curs.execute('''select rsvps from events where ename = %s and edate = %s''', (name, date,))
    return curs.fetchone()
    
def getPeople(curs, name, date):
    '''return people who have rsvpd to the event with the given name and date'''
    curs.execute('''select name from user inner join rsvps on user.username = rsvps.uname 
                    where ename = %s and edate = %s''', (name, date,))
    return curs.fetchall()
    
# ================================================================

