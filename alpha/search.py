# Riann Tang
import sys
import MySQLdb

# ================================================================

def search (curs, search_items):
    compares = ' and '.join([ ' {col} like %s '.format(col=c) for c in search_items[0] ]) 
    
    if "iname" in compares:
        curs.execute('''select user.name, user.nickname, user.classyear 
                 from user inner join industry on username=pid
                 where ''' + compares, search_items[1])
    else:
        curs.execute('''select name, nickname, classyear 
                 from user where ''' + compares, search_items[1])
    return curs.fetchall()
    
def preference(curs, username):
    curs.execute('''select * from user where name = %s''',
                  [username])
    return curs.fetchone()


