# Riann Tang

import sys
import MySQLdb
import cs304auth

def getConn(db):
    conn = cs304auth.mysqlConnectCNF(db='lounge_db')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs