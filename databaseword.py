import sqlite3
conn=sqlite3.connect("words.db",check_same_thread=False)
c=conn.cursor()
def creatdatabase():
    c.execute('''
    CREATE TABLE IF NOT EXISTS words(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT COLLATE NOCASE
    )
    ''')
    conn.commit()
    #conn.close()
def showallwords():
    c.execute("SELECT * FROM words")
    conn.commit()
    return c.fetchall()
    #c.close()
def searchbyword(word):
    c.execute("SELECT * FROM words WHERE word=? LIMIT 1",(word,))
    if c.fetchone():
        c.execute("SELECT * FROM words WHERE word=?",(word,))
    else:
        print("Your word could not be found")
    conn.commit()
    #c.close()
def searchbyid(id1):
    c.execute("SELECT * FROM words WHERE id=? LIMIT 1",(id1,))
    if c.fetchone():
        c.execute("SELECT * FROM words WHERE id=?",(id1,))
        conn.commit()
        return c.fetchall()[0][1]
        #c.close()
    else:
        print("Your id could not be found")
def add(word):
    c.execute("INSERT into words values(?,?)",(None,word))
    c.execute("SELECT * FROM words WHERE word=?",(word,))
    conn.commit()
    #c.close()
def remove(word):
    c.execute("SELECT * from words WHERE word=?",(word,))
    if c.fetchone():
        c.execute("DELETE from words WHERE word=?",(word,))
        conn.commit()
        return True
        #c.close()
    else:
        return False
def lenall():
    c.execute("SELECT * FROM words")
    allitem=c.fetchall()
    return len(allitem)
def creatpersondatabase(personid):
    c.execute('''
    CREATE TABLE IF NOT EXISTS "{}"(
        word TEXT COLLATE NOCASE
    )
    '''.format(personid.replace('"', '""')))
    conn.commit()
def addperson(personid,word):
    c.execute('''INSERT into "{}" values(?)'''.format(personid.replace('"', '""')),(word,))
    c.execute('''SELECT * FROM "{}" WHERE word=?'''.format(personid.replace('"', '""')),(word,))
    conn.commit()
def findwordperson(personid,word):
    c.execute('''SELECT * FROM "{}" WHERE word=?'''.format(personid.replace('"', '""')),(word,))
    if c.fetchone():
        return True
        #c.close()
    else:
        return False
def removepersondatabase(personid):
    c.execute('''SELECT * from "{}" '''.format(personid.replace('"', '""')))
    if c.fetchone():
        c.execute('''DELETE from "{}" '''.format(personid.replace('"', '""')))
        conn.commit()
        return True
        #c.close()
    else:
        return False