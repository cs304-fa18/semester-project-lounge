# Lauren Tso

import sys
import MySQLdb

# ================================================================

# return the connection to MySQLdb for particular user
def getConn(db):
    conn =  MySQLdb.connect(host='localhost',
                           user='ltso',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn

def getEvent(conn, name, date):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from events where ename = %s and edate = %s''', (name, date,))
    return curs.fetchone()
                           
def getEvents(conn, approved):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from events where approved = %s and edate >= current_timestamp()
                    order by edate asc''', (approved,))
    return curs.fetchall()
    
def getPastEvents(conn, approved):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from events where approved = %s and edate < current_timestamp()
                    order by edate asc''', (approved,))
    return curs.fetchall()
    
def checkEvent(conn, name, date):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select count(*) as count from events where ename = %s and edate = %s''', (name, date,))
    row = curs.fetchone()
    return row['count'] > 0
    
def submitEvent(conn, name, city, state, country, desc, date, uname):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into events(ename, city, state, country, description, edate, approved, pid) 
                    values(%s, %s, %s, %s, %s, %s, 0, %s)''', (name, city, state, country, desc, date, uname,))
                    
def approveEvent(conn, name, date):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''update events set approved = 1 where ename = %s and edate = %s''', (name, date,))

def deleteEvent(conn, name, date):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''delete from events where ename = %s and edate = %s''', (name, date,))

def updateRSVP(conn, name, date, uname):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into rsvps(uname, ename, edate) values(%s, %s, %s)''', (uname, name, date,))
    curs.execute('''update events set rsvps = rsvps + 1 where ename = %s and edate = %s''', (name, date,)) # need to inner join on rsvps

def getRSVP(conn, name, date):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select rsvps from events where ename = %s and edate = %s''', (name, date,))
    return curs.fetchone()
    
def getPeople(conn, name, date):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select name from user inner join rsvps on user.username = rsvps.uname 
                    where ename = %s and edate = %s''', (name, date,))
    return curs.fetchall()
    
# ================================================================

if __name__ == '__main__':
    conn = getConn('wmdb')
