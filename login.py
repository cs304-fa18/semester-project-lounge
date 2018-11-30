import sys
import MySQLdb

def getConn(db):
    conn =  MySQLdb.connect(host='localhost',
                           user='ltso',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn

def findUser(name, rowType='dictionary'):
    conn = getConn("wmdb")
    if rowType =='tuple':
        curs = conn.cursor()
    elif rowType =='dictionary':
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('''select * from person where name = %s''', [name])
    return curs.fetchone()


def insert(name, email, username, password, nickname, phnum, classyear, sprefs, user_type='regular'):
    conn = getConn("wmdb")
    curs = conn.cursor()
    return curs.execute('''insert into user(name,email,username, password
             nickname, phnum, classyear, user_type, spref) values 
             (%s, %s, %s, %s)''', [name, email, username, password, nickname, phnum, \
             classyear, user_type, sprefs])



