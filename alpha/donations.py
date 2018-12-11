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

def submitDonation(curs, uname, item, description):
    """Insert a new donation into the donation table"""
    curs.execute('''insert into donation (pid, item, description) values (%s, %s, %s)''', 
    (uname, item, description,))

def getName(curs, uname):
    """Return the name of given user"""
    curs.execute('''select name from user where username=%s''',( uname,))
    return curs.fetchone()

def getOldDonations(curs):
    """Return all donations marked as read"""
    curs.execute('''select * from donation where seen=1''')
    return curs.fetchall()

def getNewDonations(curs):
    """"Return all donations marked as unread"""
    curs.execute('''select * from donation where seen=0''')
    return curs.fetchall()

def mark(curs, did, seen):
    """Mark donations as either read or unread
    
    Arguments:
    Seen -- A boolean represented as a bit set to either 0 or 1
    """
    curs.execute('''update donation set seen=%s where did =%s''', 
    (seen, did,))
