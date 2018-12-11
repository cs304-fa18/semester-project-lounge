# Riann Tang

import sys
import MySQLdb

def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='rianntang',
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

def getSenderHist(curs, user):
    """Return the name of people user has messaged."""
    curs.execute('''select receiver from messages where sender=%s''', (user,))
    return curs.fetchall()

def getReceiveHist(curs,user):
    """Return the name of people user has recieved messages from."""
    curs.execute('''select sender from messages where receiver=%s''', (user,))
    return curs.fetchall()

def getName(curs, user):
    """Return the name of the given user."""
    curs.execute('''select name from user where username=%s''', (user,))
    return curs.fetchone()
   
def getMessageHistory(curs, user):
    """Return all messages user has sent and recieved messages from"""
    sendHist = getSenderHist(curs, user)
    receiveHist=getReceiveHist(curs, user)
    allMs = sendHist+receiveHist
    distinctMs = []
    for i in range (0, len(allMs)):
        if allMs[i].has_key('receiver'):
            if allMs[i]['receiver'] not in distinctMs:
                distinctMs.append(allMs[i]['receiver'])
        if allMs[i].has_key('sender'):
            if allMs[i]['sender'] not in distinctMs:
                distinctMs.append(allMs[i]['sender'])
    mHist = {}
    for i in range (0,len(distinctMs)):
        name = getName(curs, distinctMs[i])
        mHist[distinctMs[i]] = name['name']
    return mHist

def getLastM(curs, user1, user2):
    """Return most recent message between two given users"""
    curs.execute('''select message from messages where (sender=%s and receiver=%s) or 
    (sender=%s and receiver=%s) order by mid desc limit 1''',(user1,user2,user2,user1,))
    return curs.fetchone()

def getMessages(curs, user1, user2):
    """Return all messages between two given users"""
    curs.execute('''select message, sender from messages where (sender=%s and receiver=%s) 
    or (sender=%s and receiver=%s)''',(user1, user2, user2, user1,))
    return curs.fetchall()

def sendMessage(curs, sender, receiver, msg):
    "Insert messages into messages table"
    curs.execute('''insert into messages (sender, receiver, message) values 
    (%s,%s,%s)''', (sender, receiver, msg,))
    