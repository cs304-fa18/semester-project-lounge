# Riann Tang

import sys
import MySQLdb
import cs304auth

def getConn():
    conn =  MySQLdb.connect(host='localhost',
                           user='rianntang',
                           passwd='',
                           db='c9')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    conn.autocommit(True)
    return curs