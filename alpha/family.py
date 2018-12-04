# Lauren Tso

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
                           
def getAll(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select family.name, user.name as uname, user.classyear from family inner 
                    join user on family.member = user.username''')
    return curs.fetchall()
    
# ================================================================

if __name__ == '__main__':
    conn = getConn('c9')
