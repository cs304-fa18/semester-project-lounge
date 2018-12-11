# Riann Tang

import sys
import MySQLdb

def submitFeedback(curs, uname, date, subject, message):
    """Insert a new feedback into the feedback table"""
    curs.execute('''insert into feedback (subject, message, edate, pid) values (%s, %s, %s, %s)''',
    (subject, message, date, uname,))

def viewFeedback(curs):
    """Return all feedback"""
    curs.execute('''select * from feedback''')
    return curs.fetchall()