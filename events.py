#!/usr/bin/python2.7

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
                           
def getEvents(conn, approved):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from events where approved = %s order by edate asc''', (approved,))
    return curs.fetchall()
    
def submitEvent(conn, name, city, state, country, desc, date):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    print(name, city, state, country, desc, date)
    curs.execute('''insert into events(ename, city, state, country, description, edate, approved) 
                    values(%s, %s, %s, %s, %s, %s, 0)''', (name, city, state, country, desc, date,))

# ================================================================

if __name__ == '__main__':
    conn = getConn('wmdb')

