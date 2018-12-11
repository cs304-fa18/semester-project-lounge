import sys
import MySQLdb



def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn


def search (search_items):
    print "+++++++++++++++"
    print "search item", search_items
    conn = getConn("c9")
    
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    compares = ' and '.join([ ' {col} like %s '.format(col=c) for c in search_items[0] ]) 
    
    if "iname" in compares:
        curs.execute('''select user.name, user.nickname, user.classyear 
                 from user inner join industry on username=pid
                 where ''' + compares, search_items[1])
    else:
        curs.execute('''select name, nickname, classyear 
                 from user where ''' + compares, search_items[1])
    
    return curs.fetchall()
    
def preference(username):
    conn = getConn("c9")
    curs = conn.cuursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from user where name = %s''',
                  [username])
    return curs.fetchone()

def industry(username):
    conn = getConn("c9")
    curs = conn.cuursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from industry where pid = %s''',
                  [username])
    return curs.fetchone()

    

    
if __name__ == '__main__':
    x =search([('name'), ('Tam')])
    y =search([('name','classyear'), ('Tam', '2019')])
    