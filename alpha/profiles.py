# Riann Tang
import sys
import MySQLdb

# ================================================================

def checkPerson(curs, uname):
    curs.execute('''select * from user where username=%s''', (uname,))
    return curs.fetchone
    
def getSecurityPrefs(curs, uname):
    """Returns the security preferences of given user"""
    curs.execute('''select sprefs from user where username=%s''', (uname, ))
    return curs.fetchone()
    
def getBasicInfo(curs, uname):
    """Return the name, nickname and classyear of given user"""
    curs.execute('''select username, name, nickname, classyear from user where username=%s''', (uname, ))
    return curs.fetchone()
    
def getIndustry(curs, uname):
     """Return the industry type of the given user"""
     curs.execute('''select iname from industry where pid=%s''', (uname, ))
     return curs.fetchone()
     
def getTeam(curs, uname):
    """Return the team name, type, city, state and country of given user"""
    curs.execute('''select tname, nearestcity, state, country from team where pid=%s''', (uname, ))
    return curs.fetchone()
    
def getContactInfo(curs, uname):
    """Return the email and phone number of given user"""
    curs.execute('''select email, phnum from user where username=%s''', (uname, ))
    return curs.fetchone()

def getYear(curs, uname):
    """Return the classyear of given user"""
    curs.execute('''select classyear from user where username=%s''', (uname, ))
    return curs.fetchone()
    
def getOverlap(curs, uname1, uname2):
    """Return 1 if there is an overlap in time at Wellesley, 0 if not"""
    olap = 1
    year1 = int(getYear(curs, uname1)['classyear'])
    year2 = int(getYear(curs, uname2)['classyear'])
    for i in range(4):
        if (year1 + i) == year2:
            olap = 1
        if (year1 - i) == year2:
            olap = 1
    return olap