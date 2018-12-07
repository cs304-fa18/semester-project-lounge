# Riann Tang

import sys
import MySQLdb

def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='ltso',
                           passwd='',
                           db=db)
    conn.autocommit(True) # Necessary to alter the wmdb database
    return conn

def cursor(db, rowType='dictionary'): 
    conn = getConn(db)
    '''Returns a list of rows, 
    either as dictionaries (the default) or tuples'''
    if rowType == 'tuple':
        curs = conn.cursor()
    elif rowType == 'dictionary':
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs

def submitFeedback(curs, uname, date, subject, message):
    curs.execute('''insert into feedback (subject, message, edate, pid) values (%s, %s, %s, %s)''',
    (subject, message, date, uname,))

def viewFeedback(curs):
    curs.execute('''select * from feedback''')
    return curs.fetchall()