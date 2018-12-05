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

def getFamily(conn, searchterm):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    names_dict = findFamily(conn, searchterm)
    names = [name['name'] for name in names_dict]
    wildcard = tuple(names)
    curs.execute('''select family.name, user.name as uname, user.classyear from family 
                    inner join user on family.predecessor = user.username 
                    or family.member = user.username having family.name in %s
                    order by user.classyear''', (wildcard,))
    return curs.fetchall()

# need to inner join to search user name instead of username
def findFamily(conn, name):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    key = '%' + name + '%' # format the wildcard for sql search
    curs.execute('''select family.name, user.name from family inner join user on 
                    family.predecessor = user.username 
                    or family.member = user.username
                    where user.name like %s''', (key,))
    return curs.fetchall()
    
# ================================================================

if __name__ == '__main__':
    conn = getConn('c9')
