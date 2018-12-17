# Riann Tang
import sys
import MySQLdb

# ================================================================

''' 
Search for members in the database by name, nickname, classyear and industry
'''
def search (curs, search_items):
    '''Searches for profiles by name, nickname and class year'''
   # adds nickname to the query if name is in there
    if "name" in search_items[0]:
        items = [search_items[1][0]] +list(search_items[1])
        name = ['(name like %s or nickname like %s)']
        compares =' and '.join(name+[ ' {col} like %s '.format(col=c) \
        for c in search_items[0][1:]])
    else: 
        items = search_items[1]
        compares = ' and '.join([ ' {col} like %s '.format(col=c) \
        for c in search_items[0]])
        
    #sees if an industry is in the query 
    if "iname" in compares:
        curs.execute('''select user.username, user.name, user.nickname, user.classyear 
                 from user inner join industry on username=pid
                 where ''' + compares, items)
    else:
        curs.execute('''select username, name, nickname, classyear 
                 from user where ''' + compares, items)
    
    return curs.fetchall()
   
   

