# Lauren Tso

import sys
import MySQLdb

# ================================================================

def getFamily(curs, names_dict):
    '''returns all given family names and members with their given name'''
    names = [name['name'] for name in names_dict]
    wildcard = tuple(names)
    curs.execute('''select family.name, user.name as uname, user.classyear from family 
                    inner join user on family.predecessor = user.username 
                    or family.member = user.username having family.name in %s
                    order by user.classyear''', (wildcard,))
    return curs.fetchall()
    

def findFamily(curs, searchterm):
    '''returns all families with a member that matches the searchterm'''
    key = '%' + searchterm + '%' # format the wildcard for sql search
    curs.execute('''select family.name, user.name from family inner join user on 
                    family.predecessor = user.username 
                    or family.member = user.username
                    where user.name like %s''', (key,))
    return curs.fetchall()