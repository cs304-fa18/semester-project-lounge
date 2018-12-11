# Lauren Tso

import sys
import MySQLdb

# ================================================================

def getFamily(curs, searchterm):
    names_dict = findFamily(curs, searchterm)
    names = [name['name'] for name in names_dict]
    wildcard = tuple(names)
    curs.execute('''select family.name, user.name as uname, user.classyear from family 
                    inner join user on family.predecessor = user.username 
                    or family.member = user.username having family.name in %s
                    order by user.classyear''', (wildcard,))
    return curs.fetchall()
    

# need to inner join to search user name instead of username
def findFamily(curs, name):
    key = '%' + name + '%' # format the wildcard for sql search
    curs.execute('''select family.name, user.name from family inner join user on 
                    family.predecessor = user.username 
                    or family.member = user.username
                    where user.name like %s''', (key,))
    return curs.fetchall()
    
