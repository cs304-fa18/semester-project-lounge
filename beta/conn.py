# Riann Tang

import sys
import MySQLdb
import cs304auth

def getConn():
    conn =  MySQLdb.connect(host='localhost',
                           user='ltso',
                           passwd='',
                           db='lounge_db')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    conn.autocommit(True)
    return curs