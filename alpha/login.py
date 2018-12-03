import sys
import MySQLdb

def getConn(db):
    conn =  MySQLdb.connect(host='localhost',
                           user='ltso',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn

def findUser(conn, username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from user where username = %s''', [username,])
    return curs.fetchone()

def getUserType(conn, username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select user_type from user where username = %s''', [username,])
    return curs.fetchone()

def insertUser(conn, name, email, username, password, nickname, phnum, classyear, sprefs):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs.execute('''insert into user(name, email, username, password,
             nickname, phnum, classyear, user_type, sprefs) values 
             (%s, %s, %s, %s, %s, %s, %s, "regular", %s)''', [name, email, username, password, nickname, phnum,
             classyear, sprefs,])

def insertIndustry(conn, username, industry):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs.execute('''insert into industry(pid, iname) values (%s, %s)''', [username, industry,])

def insertFamily(conn, username, family, pred):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs.execute('''insert into family(memeber, name, predecessor) values (%s, %s, %s)''', [username, family, pred,])

def insertTeam(conn, username, team, ttype, ncity, state, country):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    return curs.execute('''insert into team(pid, tname, `type`, nearestcity, state, country) 
                           values (%s, %s, %s, %s, %s, %s)''', [username, team, ttype, ncity, state, country,])
