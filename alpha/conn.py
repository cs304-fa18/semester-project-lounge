# Riann Tang

import sys
import MySQLdb
import cs304auth

def getConn():
    conn =  MySQLdb.connect(host='localhost',
                           user='ltso',
                           passwd='',
                           db='c9')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs