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

# Inserts donations into the donation table    
def submitDonation(curs, uname, item, description):
    curs.execute('''insert into donation (pid, item, description) values (%s, %s, %s)''', 
    (uname, item, description,))

# Gets the name of a person from the username
def getName(curs, uname):
    curs.execute('''select name from user where username=%s''',( uname,))
    return curs.fetchone()

# View all donations marked as read
def getOldDonations(curs):
    curs.execute('''select * from donation where seen=1''')
    return curs.fetchall()

# View all donations marked as unread
def getNewDonations(curs):
    curs.execute('''select * from donation where seen=0''')
    return curs.fetchall()

# Mark donations as read or unread
def mark(curs, did, seen):
    curs.execute('''update donation set seen=%s where did =%s''', 
    (seen, did,))
