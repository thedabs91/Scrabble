# This is a file that will take my current lexicon, and convert it to a table in my database.

import sqlite3
# Set `db_file` equal to: 'Scrabble_Database.db'
def db_connector(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return(conn)
    except sqlite3.Error as e:
        print(e)
    
    return(None)

def create_table(conn, create_table_sql):
    """ creates a table from the 'create_table_sql' statement
    :param conn: a connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


# I will not worry about Collins, for now.
def create_entry(conn, entryrow, lexicon = 'twl'):
    #Creating a new gram
    sql = 'INSERT INTO lexicon_' + lexicon +\
          '''(gram, word, length, score, vowels, threeplus, jqxz, remfirst, remlast, fhook, bhook)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entryrow)
    return(cur.lastrowid)


def alphasort(string):
    list = []
    for ltr in string:
        list.append(ltr)
    list.sort()
    output = ''
    for ltr in list:
        output = output + ltr
    return(output)

# Opening the database
database = "/home/david/Documents/Common Stuff/PythonPrograms/Scrabble/Users/database.db"
conn = db_connector(database)

# First step: creating the table

def lex_table(lexicon):
    lexicon_table = 'CREATE TABLE IF NOT EXISTS lexicon_' + lexicon +\
                    	'''(gram text NOT NULL,
                            word text PRIMARY KEY,
                            length integer,
                            score integer,
                            vowels integer,
                            threeplus integer,
                            jqxz integer,
                            remfirst integer,
                            remlast integer,
                            fhook text,
                            bhook text
                            );'''
    
    if conn is not None:
        create_table(conn, lexicon_table)




# Second Step: adding the words

def multicount(string, ltrs):
    output = 0
    for ltr in ltrs:
        output += string.count(ltr)
    return (output)


def lex_db(lexicon):
    file = open('Words/UpdatedDic_' + lexicon, 'r')
    x = 1
    for line in file:
        line = line.rstrip('\n')
        line = line.split(',')
        length = len(line[0])
        nv = line[0].count('A') + line[0].count('E') + line[0].count('I') + \
            line[0].count('O') + line[0].count('U')
        njqxz = line[0].count('J') + line[0].count('Q') + line[0].count('X') + line[0].count('Z')
        ntp = multicount(line[0], 'BCFHKMPVWY') + njqxz
        pts = nv + multicount(line[0], 'LNRST') + 2*multicount(line[0], 'DG') +\
              3*multicount(line[0], 'BCMP') + 4*multicount(line[0], 'FHVWY') + 5*line[0].count('K') +\
              8*multicount(line[0], 'JX') + 10*multicount(line[0],'QZ')
        gram = alphasort(line[0])
        with conn:
            entry = (gram, line[1], length, pts, nv, ntp, njqxz, int(line[4]=='y'), int(line[5]=='y'), line[2], line[3])
            create_entry(conn, entry, lexicon = lexicon)
        if x%10000 == 0:
            print(x)
        x += 1
    print(x)
    file.close()

# This seems to have worked!

## To use the function, I recommend specifying the word list that you want in the file.

# This seems to have worked!
