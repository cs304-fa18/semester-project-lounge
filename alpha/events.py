# Lauren Tso

import sys
import MySQLdb

# ================================================================
                           
def getEvents(curs, approved):
    curs.execute('''select * from events where approved = %s and edate >= current_timestamp()
                    order by edate asc''', (approved,))
    return curs.fetchall()
    
def getPastEvents(curs, approved):
    curs.execute('''select * from events where approved = %s and edate < current_timestamp()
                    order by edate asc''', (approved,))
    return curs.fetchall()
    
def checkEvent(curs, name, date):
    curs.execute('''select count(*) as count from events where ename = %s and edate = %s''', (name, date,))
    row = curs.fetchone()
    return row['count'] > 0
    
def submitEvent(curs, name, city, state, country, desc, date, uname):
    curs.execute('''insert into events(ename, city, state, country, description, edate, approved, pid) 
                    values(%s, %s, %s, %s, %s, %s, 0, %s)''', (name, city, state, country, desc, date, uname,))
                    
def approveEvent(curs, name, date):
    curs.execute('''update events set approved = 1 where ename = %s and edate = %s''', (name, date,))

def deleteEvent(curs, name, date):
    curs.execute('''delete from events where ename = %s and edate = %s''', (name, date,))
    
def updateRSVP(curs, name, date):
    curs.execute('''update events set rsvps = rsvps + 1 where ename = %s and edate = %s''', (name, date,))

def getRSVP(curs, name, date):
    curs.execute('''select rsvps from events where ename = %s and edate = %s''', (name, date,))
    return curs.fetchone()