import sys
import MySQLdb

def findUser(curs, username):
    curs.execute('''select * from user where username = %s''', [username,])
    return curs.fetchone()

def getUserType(curs, username):
    curs.execute('''select user_type from user where username = %s''', [username,])
    return curs.fetchone()

def insertUser(curs, name, email, username, password, nickname, phnum, classyear, sprefs):
    return curs.execute('''insert into user(name, email, username, password,
             nickname, phnum, classyear, user_type, sprefs) values 
             (%s, %s, %s, %s, %s, %s, %s, "regular", %s)''', [name, email, username, password, nickname, phnum,
             classyear, sprefs,])

def insertIndustry(curs, username, industry):
    return curs.execute('''insert into industry(pid, iname) values (%s, %s)''', [username, industry,])

def insertFamily(curs, username, family, pred):
    return curs.execute('''insert into family(member, name, predecessor) values (%s, %s, %s)''', [username, family, pred,])

def insertTeam(curs, username, team, ttype, ncity, state, country):
    return curs.execute('''insert into team(pid, tname, `type`, nearestcity, state, country) 
                           values (%s, %s, %s, %s, %s, %s)''', [username, team, ttype, ncity, state, country,])
