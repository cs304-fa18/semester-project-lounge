import sys
import MySQLdb

def findUser(curs, username):
    curs.execute('''select username from user where username = %s''', [username,])
    return curs.fetchone()

def insertUser(curs, email, username, password, sprefs):
    curs.execute('''insert into user(email, username, password, user_type, sprefs) values 
                    (%s, %s, %s, "regular", %s)''', [email, username, password, sprefs,])

def updateUser(curs, username, name, nickname, phnum, classyear):
    curs.execute('''update user set name=%s, nickname=%s, phnum=%s, classyear=%s where
                    username=%s''', [name, nickname, phnum, classyear, username,])

def getPassword(curs, username):
    curs.execute('select * from user where username = %s', [username,])
    return curs.fetchone()
                    
def insertIndustry(curs, username, industry):
    return curs.execute('''insert into industry(pid, iname) values (%s, %s)''', [username, industry,])

def insertFamily(curs, username, family, pred):
    return curs.execute('''insert into family(member, name, predecessor) values (%s, %s, %s)''', [username, family, pred,])

def insertTeam(curs, username, team, ttype, ncity, state, country):
    return curs.execute('''insert into team(pid, tname, `type`, nearestcity, state, country) 
                           values (%s, %s, %s, %s, %s, %s)''', [username, team, ttype, ncity, state, country,])
